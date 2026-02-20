"""
Analysis service - handles follower analysis and interaction scoring.
Follows Single Responsibility Principle: ONLY handles analysis logic.
"""
from typing import Dict, List
import logging

from integrations.interfaces import InstagramFollowerInterface, SessionStoreInterface
from models.domain import (
    InteractionScoreModel,
    NonFollowerAnalysisResult,
    FollowRelationshipModel,
    PostModel
)
from models.exceptions import SessionNotFoundError, NotAuthenticatedError

logger = logging.getLogger(__name__)


class AnalysisService:
    """
    Service for analyzing followers and calculating interaction scores.
    Implements the core business logic for non-follower detection and ranking.
    """

    def __init__(
        self,
        session_store: SessionStoreInterface,
        max_results: int = 100,
        posts_to_analyze: int = 12
    ):
        """
        Initialize analysis service.

        Args:
            session_store: Session storage implementation
            max_results: Maximum number of non-followers to return (default 100)
            posts_to_analyze: Number of posts to analyze per account (default 12)
        """
        self.session_store = session_store
        self.max_results = max_results
        self.posts_to_analyze = posts_to_analyze

    def analyze_non_followers(self, session_token: str) -> NonFollowerAnalysisResult:
        """
        Analyze user's account and return ranked list of non-followers.

        This is the main analysis flow:
        1. Fetch followers and following lists
        2. Calculate who doesn't follow back
        3. Calculate interaction scores for each non-follower
        4. Sort by interaction score (ascending - least interaction first)
        5. Return top N results

        Args:
            session_token: User's session token

        Returns:
            NonFollowerAnalysisResult with ranked non-followers

        Raises:
            SessionNotFoundError: If session is invalid or expired
            NotAuthenticatedError: If not authenticated
        """
        # Retrieve session
        session = self.session_store.get_session(session_token)
        if not session:
            raise SessionNotFoundError("Session not found or expired. Please log in again.")

        instagram_client: InstagramFollowerInterface = session["client"]
        user_id = session["user_id"]

        logger.info(f"Starting analysis for user {user_id}")

        # Step 1: Fetch followers and following
        logger.info("Fetching followers...")
        followers = instagram_client.get_followers(user_id)

        logger.info("Fetching following...")
        following = instagram_client.get_following(user_id)

        # Step 2: Calculate non-followers (people I follow who don't follow me back)
        non_followers = {
            uid: user
            for uid, user in following.items()
            if uid not in followers
        }

        logger.info(
            f"Analysis summary: "
            f"{len(following)} following, "
            f"{len(followers)} followers, "
            f"{len(non_followers)} non-followers"
        )

        # Step 3: Calculate interaction scores
        logger.info(f"Calculating interaction scores for {len(non_followers)} non-followers...")
        scored_non_followers = self._calculate_interaction_scores(
            instagram_client=instagram_client,
            my_user_id=user_id,
            non_followers=non_followers
        )

        # Step 4: Sort by interaction score (ascending - lowest first)
        scored_non_followers.sort(key=lambda x: x.total_score)

        # Step 5: Limit to max results
        results_to_show = scored_non_followers[:self.max_results]

        logger.info(f"Returning top {len(results_to_show)} results")

        return NonFollowerAnalysisResult(
            total_following=len(following),
            total_followers=len(followers),
            total_non_followers=len(non_followers),
            non_followers_shown=len(results_to_show),
            results=results_to_show
        )

    def _calculate_interaction_scores(
        self,
        instagram_client: InstagramFollowerInterface,
        my_user_id: int,
        non_followers: Dict[int, FollowRelationshipModel]
    ) -> List[InteractionScoreModel]:
        """
        Calculate interaction scores for non-followers.

        IMPORTANT: This measures MY activity on THEIR posts.
        The score answers: How much have I engaged with this person's content?

        Args:
            instagram_client: Instagram client for API calls
            my_user_id: My Instagram user ID
            non_followers: Dictionary of non-followers to analyze

        Returns:
            List of InteractionScoreModel with calculated scores
        """
        results = []

        for target_user_id, target_user in non_followers.items():
            score = self._calculate_single_user_score(
                instagram_client=instagram_client,
                my_user_id=my_user_id,
                target_user_id=target_user_id,
                target_user=target_user
            )
            results.append(score)

        return results

    def _calculate_single_user_score(
        self,
        instagram_client: InstagramFollowerInterface,
        my_user_id: int,
        target_user_id: int,
        target_user: FollowRelationshipModel
    ) -> InteractionScoreModel:
        """
        Calculate interaction score for a single user.

        Args:
            instagram_client: Instagram client for API calls
            my_user_id: My Instagram user ID
            target_user_id: Target user's Instagram ID
            target_user: Target user's relationship model

        Returns:
            InteractionScoreModel with calculated scores
        """
        likes_count = 0
        comments_count = 0

        try:
            # Fetch target user's posts (not mine - THEIR posts)
            posts = instagram_client.get_user_posts(target_user_id, count=self.posts_to_analyze)

            logger.debug(f"Analyzing {len(posts)} posts for user {target_user.username}")

            for post in posts:
                # Check if I liked this post
                likers = instagram_client.get_post_likers(post.post_id)
                if my_user_id in likers:
                    likes_count += 1

                # Check if I commented on this post
                comments = instagram_client.get_post_comments(post.post_id)
                if any(comment["user_id"] == my_user_id for comment in comments):
                    comments_count += 1

        except Exception as e:
            logger.warning(f"Could not analyze posts for {target_user.username}: {str(e)}")
            # Continue with zero scores if we can't analyze this user

        # Create interaction score model
        score = InteractionScoreModel(
            user_id=target_user_id,
            username=target_user.username,
            full_name=target_user.full_name,
            profile_pic_url=target_user.profile_pic_url,
            likes_count=likes_count,
            comments_count=comments_count,
            total_score=0
        )

        score.calculate_total_score()

        logger.debug(
            f"Score for {target_user.username}: "
            f"{likes_count} likes, {comments_count} comments, total: {score.total_score}"
        )

        return score
