from typing import Dict, List, Optional
import httpx
import tweepy
from facebook import GraphAPI
from datetime import datetime

from src.config import settings


class SocialPublisher:
    """Multi-platform social media publisher"""

    def __init__(self):
        self.meta_api = None
        self.twitter_api = None
        self.linkedin_api = None

        # Initialize APIs if credentials are available
        if settings.meta_app_id and settings.meta_app_secret:
            # Meta API initialization will happen per-user with access tokens
            pass

        if settings.twitter_api_key and settings.twitter_api_secret:
            # Twitter API initialization will happen per-user with access tokens
            pass

    async def publish(
        self,
        content_id: str,
        platform: str,
        user_id: str,
        account_id: str,
        content: Optional[Dict] = None,
    ) -> Dict:
        """Publish content to specified platform

        Args:
            content_id: Content ID
            platform: Platform name (instagram, facebook, twitter, linkedin)
            user_id: User ID
            account_id: Social media account ID
            content: Content dictionary with text, media, etc.

        Returns:
            Publication result with post ID and URL
        """

        # In a real implementation, you would:
        # 1. Fetch content from database using content_id
        # 2. Retrieve user's access token for the platform
        # 3. Call the appropriate publishing method

        publishers = {
            "instagram": self.publish_instagram,
            "facebook": self.publish_facebook,
            "twitter": self.publish_twitter,
            "linkedin": self.publish_linkedin,
            "tiktok": self.publish_tiktok,
        }

        publisher = publishers.get(platform.lower())

        if not publisher:
            raise ValueError(f"Platform {platform} not supported")

        result = await publisher(content, account_id)

        return result

    async def publish_instagram(
        self, content: Dict, account_id: str, access_token: str = None
    ) -> Dict:
        """Publish to Instagram using Meta Graph API

        Args:
            content: Dict with 'text', 'image_url', 'media_type'
            account_id: Instagram Business Account ID
            access_token: User access token

        Returns:
            Post details
        """
        if not access_token:
            raise ValueError("Instagram access token required")

        graph = GraphAPI(access_token=access_token, version="19.0")

        media_type = content.get("media_type", "IMAGE")

        try:
            if media_type == "IMAGE":
                # Create media container
                container = graph.put_object(
                    parent_object=account_id,
                    connection_name="media",
                    image_url=content["image_url"],
                    caption=content.get("text", ""),
                )

                # Publish the container
                post = graph.put_object(
                    parent_object=account_id,
                    connection_name="media_publish",
                    creation_id=container["id"],
                )

                return {
                    "status": "published",
                    "platform": "instagram",
                    "post_id": post["id"],
                    "published_at": datetime.utcnow().isoformat(),
                }

            elif media_type == "CAROUSEL":
                # Carousel album
                children = []
                for media_url in content.get("media_urls", []):
                    child = graph.put_object(
                        parent_object=account_id,
                        connection_name="media",
                        image_url=media_url,
                        is_carousel_item=True,
                    )
                    children.append(child["id"])

                # Create carousel container
                carousel = graph.put_object(
                    parent_object=account_id,
                    connection_name="media",
                    caption=content.get("text", ""),
                    media_type="CAROUSEL",
                    children=children,
                )

                # Publish
                post = graph.put_object(
                    parent_object=account_id,
                    connection_name="media_publish",
                    creation_id=carousel["id"],
                )

                return {
                    "status": "published",
                    "platform": "instagram",
                    "post_id": post["id"],
                    "type": "carousel",
                    "published_at": datetime.utcnow().isoformat(),
                }

            elif media_type == "REELS":
                # Instagram Reels
                container = graph.put_object(
                    parent_object=account_id,
                    connection_name="media",
                    media_type="REELS",
                    video_url=content["video_url"],
                    caption=content.get("text", ""),
                )

                post = graph.put_object(
                    parent_object=account_id,
                    connection_name="media_publish",
                    creation_id=container["id"],
                )

                return {
                    "status": "published",
                    "platform": "instagram",
                    "post_id": post["id"],
                    "type": "reels",
                    "published_at": datetime.utcnow().isoformat(),
                }

        except Exception as e:
            return {"status": "failed", "error": str(e), "platform": "instagram"}

    async def publish_facebook(
        self, content: Dict, page_id: str, access_token: str = None
    ) -> Dict:
        """Publish to Facebook Page

        Args:
            content: Post content
            page_id: Facebook Page ID
            access_token: Page access token

        Returns:
            Post details
        """
        if not access_token:
            raise ValueError("Facebook access token required")

        graph = GraphAPI(access_token=access_token, version="19.0")

        try:
            post_data = {"message": content.get("text", "")}

            # Add media if present
            if content.get("image_url"):
                post_data["link"] = content["image_url"]

            post = graph.put_object(
                parent_object=page_id, connection_name="feed", **post_data
            )

            return {
                "status": "published",
                "platform": "facebook",
                "post_id": post["id"],
                "published_at": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            return {"status": "failed", "error": str(e), "platform": "facebook"}

    async def publish_twitter(
        self, content: Dict, access_token: str = None, access_secret: str = None
    ) -> Dict:
        """Publish to Twitter/X

        Args:
            content: Tweet content
            access_token: User access token
            access_secret: User access token secret

        Returns:
            Tweet details
        """
        if not access_token or not access_secret:
            raise ValueError("Twitter credentials required")

        try:
            # Initialize Twitter API v2 client
            client = tweepy.Client(
                consumer_key=settings.twitter_api_key,
                consumer_secret=settings.twitter_api_secret,
                access_token=access_token,
                access_token_secret=access_secret,
            )

            text = content.get("text", "")

            # Check if it's a thread
            if content.get("is_thread") and content.get("thread_tweets"):
                # Post thread
                previous_tweet_id = None
                tweet_ids = []

                for tweet_text in content["thread_tweets"]:
                    if previous_tweet_id:
                        response = client.create_tweet(
                            text=tweet_text,
                            in_reply_to_tweet_id=previous_tweet_id,
                        )
                    else:
                        response = client.create_tweet(text=tweet_text)

                    previous_tweet_id = response.data["id"]
                    tweet_ids.append(previous_tweet_id)

                return {
                    "status": "published",
                    "platform": "twitter",
                    "post_ids": tweet_ids,
                    "type": "thread",
                    "published_at": datetime.utcnow().isoformat(),
                }
            else:
                # Single tweet
                response = client.create_tweet(text=text)

                return {
                    "status": "published",
                    "platform": "twitter",
                    "post_id": response.data["id"],
                    "published_at": datetime.utcnow().isoformat(),
                }

        except Exception as e:
            return {"status": "failed", "error": str(e), "platform": "twitter"}

    async def publish_linkedin(
        self, content: Dict, person_urn: str, access_token: str = None
    ) -> Dict:
        """Publish to LinkedIn

        Args:
            content: Post content
            person_urn: LinkedIn person URN
            access_token: User access token

        Returns:
            Post details
        """
        if not access_token:
            raise ValueError("LinkedIn access token required")

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        }

        # Prepare post data
        post_data = {
            "author": person_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": content.get("text", "")},
                    "shareMediaCategory": "NONE",
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
        }

        # Add media if present
        if content.get("image_url"):
            post_data["specificContent"]["com.linkedin.ugc.ShareContent"][
                "shareMediaCategory"
            ] = "IMAGE"
            post_data["specificContent"]["com.linkedin.ugc.ShareContent"]["media"] = [
                {
                    "status": "READY",
                    "description": {"text": content.get("text", "")},
                    "media": content["image_url"],
                    "title": {"text": "Image"},
                }
            ]

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.linkedin.com/v2/ugcPosts",
                    headers=headers,
                    json=post_data,
                )

                if response.status_code == 201:
                    result = response.json()
                    return {
                        "status": "published",
                        "platform": "linkedin",
                        "post_id": result.get("id"),
                        "published_at": datetime.utcnow().isoformat(),
                    }
                else:
                    return {
                        "status": "failed",
                        "error": response.text,
                        "platform": "linkedin",
                    }

        except Exception as e:
            return {"status": "failed", "error": str(e), "platform": "linkedin"}

    async def publish_tiktok(
        self, content: Dict, access_token: str = None
    ) -> Dict:
        """Publish to TikTok

        Args:
            content: Video content
            access_token: User access token

        Returns:
            Post details
        """
        # TikTok API implementation
        # Note: TikTok's API requires video upload which is more complex
        return {
            "status": "not_implemented",
            "platform": "tiktok",
            "message": "TikTok publishing requires video upload workflow",
        }

    async def get_post_metrics(
        self, platform: str, post_id: str, access_token: str
    ) -> Dict:
        """Fetch post performance metrics

        Args:
            platform: Platform name
            post_id: Post ID
            access_token: Access token

        Returns:
            Metrics dict with likes, comments, shares, impressions, etc.
        """
        metrics_fetchers = {
            "instagram": self._get_instagram_metrics,
            "facebook": self._get_facebook_metrics,
            "twitter": self._get_twitter_metrics,
            "linkedin": self._get_linkedin_metrics,
        }

        fetcher = metrics_fetchers.get(platform.lower())

        if not fetcher:
            raise ValueError(f"Platform {platform} not supported")

        return await fetcher(post_id, access_token)

    async def _get_instagram_metrics(self, post_id: str, access_token: str) -> Dict:
        """Fetch Instagram post metrics"""
        graph = GraphAPI(access_token=access_token, version="19.0")

        try:
            insights = graph.get_object(
                id=post_id,
                fields="insights.metric(engagement,impressions,reach,saved)",
            )

            return {
                "platform": "instagram",
                "post_id": post_id,
                "metrics": insights.get("insights", {}),
                "fetched_at": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            return {"error": str(e)}

    async def _get_facebook_metrics(self, post_id: str, access_token: str) -> Dict:
        """Fetch Facebook post metrics"""
        graph = GraphAPI(access_token=access_token, version="19.0")

        try:
            post = graph.get_object(
                id=post_id,
                fields="likes.summary(true),comments.summary(true),shares,reactions.summary(true)",
            )

            return {
                "platform": "facebook",
                "post_id": post_id,
                "likes": post.get("likes", {}).get("summary", {}).get("total_count", 0),
                "comments": post.get("comments", {}).get("summary", {}).get("total_count", 0),
                "shares": post.get("shares", {}).get("count", 0),
                "reactions": post.get("reactions", {}).get("summary", {}).get("total_count", 0),
                "fetched_at": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            return {"error": str(e)}

    async def _get_twitter_metrics(self, tweet_id: str, access_token: str) -> Dict:
        """Fetch Twitter post metrics"""
        # Implement Twitter metrics fetching
        return {"platform": "twitter", "post_id": tweet_id}

    async def _get_linkedin_metrics(self, post_id: str, access_token: str) -> Dict:
        """Fetch LinkedIn post metrics"""
        # Implement LinkedIn metrics fetching
        return {"platform": "linkedin", "post_id": post_id}
