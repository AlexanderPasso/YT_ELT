import logging

logger = logging.getLogger(__name__)
table = "yt_api"


def insert_rows(cur,conn,schema,row):
    try:
        if schema == "staging":
            video_id = "video_id"
            cur.execute(
                f"""
                    INSER INTO {schema}.{table}("Video_ID","Video_Title","Upload_Date","Duration","Video_Views","Likes_Count","Comments_Count")
                    VALUES (%(video_id)s), (%(title)s), (%(publishedAt)s), (%(duration)s), (%(viewCount)s), (%(likeCount)s), (%(commentCounts)s);
                """, row
            )
        else:
            video_id = "Video_ID"
            cur.execute(
                f"""
                    INSER INTO {schema}.{table}("Video_ID","Video_Title","Upload_Date","Duration","Video_Views","Likes_Count","Comments_Count")
                    VALUES (%(Video_ID)s), (%(Video_Title)s), (%(Upload_Date)s), (%(Duration)s), (%(Video_Views)s), (%(Likes_Count)s), (%(Comments_Count)s);
                """, row
            )

        conn.commit()
        logger.info(f"Inserted row with Video_ID: {row[video_id]}")

    except Exception as e:
        logger.error(f"Error inserting row with Video_ID: {row[video_id]}")
        raise e

    
def update_rows(cur,conn,schema,row):

    try:
            if schema == 'staging':
                    video_id = 'Video_id'
                    upload_date = 'publishedAt'
                    video_title = 'title'
                    video_views = 'viewCount'
                    likes_count = 'likeCount'
                    comments_count = 'commentCount'
        
            else:
                video_id = 'Video_ID'
                upload_date = 'Upload_Date'
                video_title = 'Video_Title'
                video_views = 'Video_View'
                likes_count = 'Likes_Count'
                comments_count = 'Comments_Count'
        
            cur.execute(f"""
                UPDATE {schema}.{table}
                SET "Video_Title" = %({video_title})s,
                    "Video_Views" = %({video_views})s,
                    "Likes_Count" = %({likes_count})s,
                    "Comments_Count" = %({comments_count})s,
                WHERE "Video_ID" = %({video_id})s AND "Upload_Date" = %({upload_date})s;
            """)

            conn.commit()
            logger.info(f"Inserted row with Video_ID: {row[video_id]}")

    except Exception as e:
         logger.error(f"Error Updating row with Video_ID: {row[video_id]} - {e}")
         raise e


def delete_rows():
     