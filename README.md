# IIQ-Managed-Service

## Introduction
This service is used to reduce the integration time of InsightIq APIs. All the nuances required for integration are taken care of in this service. Only, need to add the configuration.

This service is listening the webhooks for most of the apis from [InsightIq](https://www.insightiq.ai) and then extract the data and store in the db.

For few products like CREATOR_SEARCH, PUBLIC_CONTENT_SEARCH, api integration is there. It’ll return the response as well as store in the db, if configured.

## Pre-requisites
[Git](https://www.atlassian.com/git/tutorials/install-git)

[InsightIq Developer Account](https://dashboard.insightiq.ai/)

[Docker](https://docs.docker.com/engine/install/)

[Docker-Compose](https://dockerlabs.collabnix.com/intermediate/workshop/DockerCompose/How_to_Install_Docker_Compose.html)

[Postgres](https://www.postgresql.org/download/)

## Integration Steps
- Clone the git repository.

- Go to the repository and open file docker-compose and start configuring it:

  - Port on which you want to expose your docker application. The docker port will always remain 8000. So, suppose, you want to expose on port 9000 then configure ports like 9000:8000

  - ENVIRONMENT: SANDBOX / STAGING / PRODUCTION
 
  - TENANT_APP_ID/TENANT_APP_SECRET:  Get them from the insightiq-developer-account for the corresponding environment.

  - SUPPORTED_PRODUCTS: Comma separated list of products which you want to integrate. Valid products are IDENTITY, IDENTITY.AUDIENCE, ENGAGEMENT, ENGAGEMENT.AUDIENCE, INCOME, ACTIVITY. This list keep on updating.
  
  - EVENT_EXECUTORS: Comma separated list of classes of event-executors to be configured. This class has to inherit the class _app.events.base_event.BaseEvent_ and can override the corresponding events. For reference, if someone wants to push the events to database, then they can configure it to _app.events.db.db_event_handler.DbEventHandler_

  - WEBHOOK_BASE_URL: The base url which you’re going to map for this docker container so that this service can listen the webhooks. This url should be whitelisted for the outside world.

  - DB_configuration: Currently, supporting only postgres-db for integration. Configure the attributes as defined in the file.

- If db-event is enabled then need to Configure the field-mapping inside the file [here](app/events/db/db_table_field_mappings.yaml). This file is currently having sample mappings. Remove whichever is not applicable.

- Go to the base directory and then build the docker-compose using following command:

  `docker-compose build`

- After the container is built, run the docker container using the following command:
 
  `docker-compose up`

- If it got started successfully, then go to the browser and open the following url:
    ```djangourlpath
    http://localhost:<port-which-you-configured>/
    ```
   

- It’ll give the output:
  ```json
  {"message": "I'm up"}
  ```


## Configuration of field-mapper.yaml file
- Format:
![field-mapper](https://github.com/insightiq-ai/iiq-managed-service/assets/135609264/32240d3c-e6e4-48c0-b0a9-44fad1fec931)


- mappings:
  - account: ← Name of the content which needs to mapped. Valid values are (account, profile, profile_audience, content, content_group, social_transaction, commerce_transaction, social_payout, commerce_payout, commerce_balance, activity_artist, activity_content, profile_search, profile_analytics, contents_information )
    - name: <your db table name>
    - schema: <your db table schema>
    - unique_key: <unique key of your db-table>
    - fields:
      - \<api response field-name\>: \<your db-table column name\>
    - value_post_processors:
      - \<your db-table column name\>: \<Full path of the method which needs to be executed which expects value as string argument\>


- api response-field-names can be referred from the doc-links below:
  - [user](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/create-a-v-1-user#response-body)
  - [account](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/get-a-v-1-account#Responses)
  - [profile](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/get-a-v-1-profile#Responses)
  - [profile_audience](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/get-a-v-1-audience#Responses)
  - [content](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/create-a-v-1-social-content-search#Responses)
  - [content_group](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/create-a-v-1-social-content-group-search#Responses)
  - [social_transaction](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/create-a-v-1-social-income-transaction-search#Responses)
  - [commerce_transaction](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/create-a-v-1-commerce-income-transaction-search#Responses)
  - [social_payout](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/create-a-v-1-social-income-payout-search#Responses)
  - [commerce_payout](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/create-a-v-1-commerce-income-payout-search#Responses)
  - [commerce_balance](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/create-a-v-1-commerce-income-balance-search#Responses)
  - [activity_artist](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/create-a-v-1-media-activity-artist-search#Responses)
  - [activity_content](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/create-a-v-1-media-activity-content-search#Responses)
  - [profile_fetch](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/list-v-1-social-creator-profiles#Responses)
  - [profile_search](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/create-a-v-1-social-creator-profile-search#Responses)
  - [profile_analytics](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/create-a-v-1-social-creator-profile-analytics#Responses)
  - [contents_information](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/create-a-v-1-social-creator-content-fetch#Responses) 
  - [publish_content](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/get-a-v-1-social-content-publish#response-body)
  - [brands](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/list-v-1-social-creator-dictionary-brands#Responses)
  - [interests](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/list-v-1-social-creator-dictionary-interests#Responses)
  - [languages](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/list-v-1-social-creator-dictionary-languages#Responses)
  - [locations](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/list-v-1-social-creator-dictionary-locations#Responses)
  - [topics](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/list-v-1-social-creator-dictionary-topics#Responses)
  - [topics_relevance](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/get-a-v-1-social-creator-dictionary-topic-relevance#Responses)
  - [userhandles](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/list-v-1-social-creator-dictionary-userhandles#Responses)
  - [profile_quick_search](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/create-a-v-1-social-creator-profile-quick-search#Responses)
  - [profile_contact_info](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/create-a-v-1-social-creator-profile-contact-info#Responses)
  - [professional_profile_analytics](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/create-a-v-1-professional-creator-profile-analytics#Responses)
  - [professional_contents_fetch](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/get-a-v-1-professional-creator-content-fetch)
  - [social_contents_fetch](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/get-a-v-1-social-creator-async-content-fetch)
  - [social_profile_analytics](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/get-a-v-1-social-creator-async-profile-analytics)
  - [audience_overlap](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/get-a-v-1-social-creator-audience-overlap)
  - [search_export](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/get-a-v-1-social-creator-profile-search-export)


## APIs
- Create User
  - This api is used to create a new user
    - **POST** <BASE-URL>/v1/users
  
      Request-body:
      ```json
      {   "name": "kushal",
          "external_id": "kushal_id4"
      }
      ```

      Response-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/create-a-v-1-user#response-body)


- Generate Sdk-Token
  - This api is used to generate the sdk-token
  - **POST** <BASE-URL>/v1/users/sdk-tokens

    Request-body:
    ```json
    {
      "user_id": "839e3c0d-f2b4-45e4-bbdf-4e6a7c790c48"
    }
    ```

    Response-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/create-a-v-1-sdk-token#response-body)
  

- APIs for products: CREATOR_SEARCH, PUBLIC_CONTENT_SEARCH
  - Fetch creator's basic profile information
    - Fetch follower count and other basic profile information of a creator using publicly available data based on available filters.
      - **GET** <BASE-URL>/v1/social/creators/profiles
    
        Query-Params: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/list-v-1-social-creator-profiles#Query-Parameters)
    
        Response-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/list-v-1-social-creator-profiles#Responses)

  - Search public profiles of creators:
    - Search for creator profiles using publicly available data based on available filters.
      - **POST** <BASE-URL>/v1/social/creators/profiles/search
    
        Request-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/create-a-v-1-social-creator-profile-search#request-body)
    
        Response-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/create-a-v-1-social-creator-profile-search#Responses)

  - Get public analytics of a profile:
    - Get analytics for creator's profile using publicly available data based on their username or link.
      - **POST** <BASE-URL>/v1/social/creators/profiles/analytics

         Request-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/create-a-v-1-social-creator-profile-analytics#request-body)

         Response-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/create-a-v-1-social-creator-profile-analytics#Responses)

  - Get public content information for a profile or single content item:
    - Retrieve the information of a profile's content or information of a single content item with the supplied content url.
      - **POST** <BASE-URL>/v1/social/creators/contents/fetch

         Request-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/create-a-v-1-social-creator-content-fetch#request-body)

         Response-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/create-a-v-1-social-creator-content-fetch#Responses)

  - Fetch a dictionary of brands.
    - Dictionary of brands for the public profiles search endpoint:
      - **GET** <BASE-URL>/v1/social/creators/dictionary/brands

         Request-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/list-v-1-social-creator-dictionary-brands#request-body)

         Response-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/list-v-1-social-creator-dictionary-brands#Responses)

  - Fetch a dictionary of interests.
    - Dictionary of interests for the public profiles search endpoint:
      - **GET** <BASE-URL>/v1/social/creators/dictionary/interests

         Request-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/list-v-1-social-creator-dictionary-interests#request-body)

         Response-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/list-v-1-social-creator-dictionary-interests#Responses)
 
  - Fetch a dictionary of languages.
    - Dictionary of languages for the public profiles search endpoint:
      - **GET** <BASE-URL>/v1/social/creators/dictionary/languages

         Request-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/list-v-1-social-creator-dictionary-languages#request-body)

         Response-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/list-v-1-social-creator-dictionary-languages#Responses)

  - Fetch a dictionary of locations.
    - Dictionary of countries for the public profiles search endpoint:
      - **GET** <BASE-URL>/v1/social/creators/dictionary/locations

         Request-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/list-v-1-social-creator-dictionary-locations#request-body)

         Response-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/list-v-1-social-creator-dictionary-locations#Responses)

  - Fetch a dictionary of topics.
    - Dictionary of topic tags for the public profiles search endpoint:
      - **GET** <BASE-URL>/v1/social/creators/dictionary/topics

         Request-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/list-v-1-social-creator-dictionary-topics#request-body)

         Response-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/list-v-1-social-creator-dictionary-topics#Responses)

  - Fetch a dictionary of relevance weights of topic tags:
    - Dictionary of relevance weights of topic tags for the public profiles search endpoint.
      - **GET** <BASE-URL>/v1/social/creators/dictionary/topics/relevance

         Request-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/get-a-v-1-social-creator-dictionary-topic-relevance#request-body)

         Response-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/get-a-v-1-social-creator-dictionary-topic-relevance#Responses)

  - Get a dictionary of userhandles for whom creator lookalikes data is available:
    - Retrieve list of userhandles matching the query text.
      - **GET** <BASE-URL>/v1/social/creators/dictionary/userhandles

         Request-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/list-v-1-social-creator-dictionary-userhandles#request-body)

         Response-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/list-v-1-social-creator-dictionary-userhandles#Responses)

  - Get public analytics of a profile:
    - Search for creator profiles using publicly available data based on available filters.
      - **POST** <BASE-URL>/v1/social/creators/profiles/quick-search

         Request-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/create-a-v-1-social-creator-profile-quick-search#request-body)

         Response-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/create-a-v-1-social-creator-profile-quick-search#Responses)

  - Get contact details of a profile:
    - Get contact details of a particular handle on Instagram, YouTube and TikTok, without fetching the analytics.
      - **POST** <BASE-URL>/v1/social/creators/profiles/contact-info

         Request-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/create-a-v-1-social-creator-profile-contact-info#request-body)

         Response-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/create-a-v-1-social-creator-profile-contact-info#Responses)

  - Get contact details of a professional:
    - Get analytics of profile using publicly available data based on their profile link.
      - **POST** <BASE-URL>/v1/professional/creators/profiles/analytics

         Request-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/create-a-v-1-professional-creator-profile-analytics#request-body)

         Response-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/create-a-v-1-professional-creator-profile-analytics#Responses)

  - Get asynchronous content fetch results for a social creator:
      - Retrieve content data asynchronously using a creator's social profile.
        - **POST** <BASE-URL>/v1/social/creators/async/contents/fetch

           Request-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/get-a-v-1-social-creator-async-content-fetch#request-body)

           Response-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/get-a-v-1-social-creator-async-content-fetch#Responses)


  - Get asynchronous content fetch results for a social creator:
      - Retrieve content data asynchronously using a creator's social profile.
        - **POST** <BASE-URL>/v1/social/creators/async/contents/fetch

           Request-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/get-a-v-1-social-creator-async-content-fetch#request-body)

           Response-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/get-a-v-1-social-creator-async-content-fetch#Responses)


  - Get asynchronous content fetch results for a social creator:
      - Retrieve content data asynchronously using a creator's social profile.
        - **POST** <BASE-URL>/v1/social/creators/async/contents/fetch

           Request-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/get-a-v-1-social-creator-async-content-fetch#request-body)

           Response-body: [Click here](https://docs.insightiq.ai/docs/api-reference/api/ref/operations/get-a-v-1-social-creator-async-content-fetch#Responses)


## Database Table Mappings


### `professional_contents_fetch_data`

This table stores the fetched content data for professional platforms.

- **Schema**: `iiq_schema`
  - **Unique Key**: `professional_contents_fetch_request_iiq_id`, `platform_content_id`
  - **Fields**:
    - `job_id`: Maps to `professional_contents_fetch_request_iiq_id`, which links the data to the request.
    - `work_platform`: Maps to platform details, including `work_platform_id`, `work_platform_name`, and `work_platform_logo_url`.
    - `profile`: Maps to profile details, including `platform_username`, `profile_url`, `external_id`, `profile_image_url`, and `is_verified`.
    - `audio_track_info`: Maps to audio track details, including `audio_track_id`, `audio_track_title`, `audio_track_artist`, and `audio_track_original`.
    - `engagement`: Maps to engagement metrics, including `like_count`, `applause_count`, `support_count`, `love_count`, `interest_count`, `laugh_count`, `comment_count`, `view_count`, and `share_count`.
    - `platform_content_id`: Maps to the unique content identifier on the platform.
    - `title`: Maps to the title of the content.
    - `format`: Maps to the format of the content.
    - `type`: Maps to the type of the content.
    - `url`: Maps to the content URL.
    - `media_url`: Maps to the media URL associated with the content.
    - `thumbnail_url`: Maps to the thumbnail URL of the content.
    - `duration`: Maps to the duration of the content.
    - `description`: Maps to the description of the content.
    - `published_at`: Maps to the publication date and time of the content.
    - `is_reposted`: Maps to whether the content is reposted.
    - `collaborators`: Maps to JSON data containing collaborator details, processed by the `cast_to_json` value processor.
    - `sponsors`: Maps to JSON data containing sponsor details, processed by the `cast_to_json` value processor.
    - `mentions`: Maps to JSON data containing mentions details, processed by the `cast_to_json` value processor.
    - `links`: Maps to JSON data containing link details, processed by the `cast_to_json` value processor.
    - `hashtags`: Maps to JSON data containing hashtag details, processed by the `cast_to_json` value processor.

  - **Value Processors**:
    - `published_at`: Casts the `published_at` field to a datetime object using the `cast_iso_formatted_string_to_datetime` processor.
    - `collaborators_json`: Casts the `collaborators` data to JSON format.
    - `sponsors_json`: Casts the `sponsors` data to JSON format.
    - `mentions_json`: Casts the `mentions` data to JSON format.
    - `links_json`: Casts the `links` data to JSON format.
    - `hashtags_json`: Casts the `hashtags` data to JSON format.

### `professional_contents_fetch_request`

This table stores the request details for fetching professional content.

- **Schema**: `iiq_schema`
  - **Unique Key**: `iiq_id`
  - **Fields**:
    - `id`: Maps to `iiq_id`, which uniquely identifies the request.
    - `status`: Maps to the current status of the request.
    - `work_platform`: Maps to platform details, including `work_platform_id`, `work_platform_name`, and `work_platform_logo_url`.
    - `profile_url`: Maps to the profile URL associated with the request.
    - `content_url`: Maps to the content URL associated with the request.


### `async_contents_fetch_data`

This table stores the fetched content data related to a social creator. The unique key for this table is a combination of `async_contents_fetch_request_iiq_id` and `platform_content_id`.
  
- Schema: `iiq_schema`
  - Fields:
    - `id`: Maps to `async_contents_fetch_request_iiq_id`
    - `work_platform`: Maps to the platform details, including `work_platform_id`, `work_platform_name`, and `work_platform_logo_url`.
    - `platform_content_id`: Maps to `platform_content_id`
    - `title`, `format`, `type`, `url`, `media_url`, `thumbnail_url`, `duration`, `description`, `published_at`, `is_reposted`
    - `profile`: Maps to profile details like `platform_username`, `profile_url`, `external_id`, `profile_image_url`, and `is_verified`
    - `audio_track_info`: Maps to audio track details such as `audio_track_id`, `audio_track_title`, `audio_track_artist`, and `audio_track_original`
    - `engagement`: Maps to engagement metrics including `like_count`, `applause_count`, `support_count`, `love_count`, `interest_count`, `laugh_count`, `comment_count`, `view_count`, `share_count`
    - `collaborators`, `sponsors`, `mentions`, `links`, `hashtags`: Handled via JSON fields with appropriate value processors
  
  - Value Processors:
    - `published_at`: Casts ISO formatted string to datetime.
    - `collaborators_json`, `sponsors_json`, `mentions_json`, `links_json`, `hashtags_json`: Cast to JSON.

### `async_contents_fetch_request`

This table stores the request details for fetching content data asynchronously.
  
- Schema: `iiq_schema`
  - Fields:
    - `id`: Maps to `iiq_id`
    - `status`: Maps to `status`
    - `work_platform`: Maps to platform details including `work_platform_id`, `work_platform_name`, `work_platform_logo_url`
    - `profile_url`, `content_url`


### `async_profile_analytics`

This table stores detailed analytics data for profiles, including various metrics and related information across different work platforms.

- **Schema**: `iiq_schema`
  - **Unique Key**: `iiq_id`
  - **Fields**:
    - `id`: Maps to `iiq_id`, which uniquely identifies the analytics record.
    - `status`: Maps to the current status of the analytics data processing.
    - `identifier`: Maps to the identifier associated with the analytics record.
    - `report_generated_at`: Maps to the timestamp when the report was generated.
    - `updated_at`: Maps to the timestamp when the record was last updated.
    - `work_platform`:
      - `id`: Maps to `work_platform_id`, which identifies the platform.
      - `name`: Maps to `work_platform_name`, which names the platform.
      - `logo_url`: Maps to `work_platform_logo_url`, which stores the platform's logo URL.
    - `profile`:
      - `platform_username`: Maps to `platform_username`, the username on the platform.
      - `url`: Maps to `profile_url`, the profile URL on the platform.
      - `image_url`: Maps to `profile_image_url`, the profile image URL.
      - `follower_count`: Maps to `profile_follower_count`, the number of followers.
      - `subscriber_count`: Maps to `profile_subscriber_count`, the number of subscribers.
      - `is_verified`: Maps to `profile_is_verified`, the verification status of the profile.
      - `full_name`: Maps to `profile_full_name`, the full name of the profile owner.
      - `introduction`: Maps to `profile_introduction`, the introduction or bio of the profile.
      - `platform_account_type`: Maps to `profile_platform_account_type`, the type of account on the platform.
      - `gender`: Maps to `profile_gender`, the gender associated with the profile.
      - `age_group`: Maps to `profile_age_group`, the age group of the profile owner.
      - `language`: Maps to `profile_language`, the language associated with the profile.
      - `average_likes`: Maps to `profile_average_likes`, the average number of likes on posts.
      - `average_comments`: Maps to `profile_average_comments`, the average number of comments on posts.
      - `average_views`: Maps to `profile_average_views`, the average number of views on posts.
      - `average_reels_views`: Maps to `profile_average_reels_views`, the average number of views on reels.
      - `engagement_rate`: Maps to `profile_engagement_rate`, the engagement rate of the profile.
      - `content_count`: Maps to `profile_content_count`, the total count of content posted by the profile.
      - `sponsored_posts_performance`: Maps to `profile_sponsored_posts_performance`, the performance metrics of sponsored posts.
      - `reputation_history`: Maps to `profile_reputation_history`, the reputation history of the profile.
      - `location`: Maps to `profile_location`, the location details of the profile.
      - `top_hashtags`: Maps to `profile_top_hashtags`, the top hashtags used by the profile.
      - `top_mentions`: Maps to `profile_top_mentions`, the top mentions made by the profile.
      - `top_interests`: Maps to `profile_top_interests`, the top interests associated with the profile.
      - `brand_affinity`: Maps to `profile_brand_affinity`, the brand affinity associated with the profile.
      - `top_contents`: Maps to `profile_top_contents`, the top content pieces posted by the profile.
      - `recent_contents`: Maps to `profile_recent_contents`, the most recent content posted by the profile.
      - `sponsored_contents`: Maps to `profile_sponsored_contents`, the sponsored content posted by the profile.
      - `lookalikes`: Maps to `profile_lookalikes`, the profiles that are lookalikes of the current profile.
      - `audience`: Maps to `profile_audience`, the audience associated with the profile.
      - `engagement_rate_histogram`: Maps to `profile_engagement_rate_histogram`, the engagement rate histogram of the profile.
      - `audience_likers`: Maps to `profile_audience_likers`, the likers in the profile's audience.
      - `contact_details`: Maps to `profile_contact_details`, the contact details associated with the profile.

  - **Value Processors**:
    - `profile_reputation_history`: Casts `profile_reputation_history` to JSON format.
    - `profile_location`: Casts `profile_location` to JSON format.
    - `profile_top_hashtags`: Casts `profile_top_hashtags` to JSON format.
    - `profile_top_mentions`: Casts `profile_top_mentions` to JSON format.
    - `profile_top_interests`: Casts `profile_top_interests` to JSON format.
    - `profile_brand_affinity`: Casts `profile_brand_affinity` to JSON format.
    - `profile_top_contents`: Casts `profile_top_contents` to JSON format.
    - `profile_recent_contents`: Casts `profile_recent_contents` to JSON format.
    - `profile_sponsored_contents`: Casts `profile_sponsored_contents` to JSON format.
    - `profile_lookalikes`: Casts `profile_lookalikes` to JSON format.
    - `profile_audience`: Casts `profile_audience` to JSON format.
    - `profile_engagement_rate_histogram`: Casts `profile_engagement_rate_histogram` to JSON format.
    - `profile_audience_likers`: Casts `profile_audience_likers` to JSON format.
    - `profile_contact_details`: Casts `profile_contact_details` to JSON format.


### `audience_overlap_data`

This table stores the results of the audience overlap calculations.

- **Schema**: `iiq_schema`
  - **Unique Key**: `id`
  - **Fields**:
    - `id`: Maps to `id`, which uniquely identifies the data.
    - `status`: Maps to the current status of the data processing.
    - `total_follower_count`: Maps to the total number of followers across all platforms.
    - `unique_follower_count`: Maps to the count of unique followers across all platforms.
    - `total_subscriber_count`: Maps to the total number of subscribers across all platforms.
    - `unique_subscriber_count`: Maps to the count of unique subscribers across all platforms.
    - `profiles`: Maps to JSON data containing details of profiles involved in the overlap, processed by the `cast_to_json` value processor.
    - `error`: Maps to any error message or details encountered during the overlap calculation.
    - `ignored_profiles`: Maps to JSON data containing details of profiles that were ignored in the overlap, processed by the `cast_to_json` value processor.

  - **Value Processors**:
    - `profiles_json`: Casts the `profiles` data to JSON format.
    - `ignored_profiles_json`: Casts the `ignored_profiles` data to JSON format.

### `audience_overlap_request`

This table stores the request details for audience overlap calculations.

- **Schema**: `iiq_schema`
  - **Unique Key**: `id`
  - **Fields**:
    - `id`: Maps to `id`, which uniquely identifies the request.
    - `identifiers`: Maps to a list of identifiers used for the audience overlap calculation.
    - `status`: Maps to the current status of the request.
    - `work_platform`: Maps to platform details including `work_platform_id`, `work_platform_name`, and `work_platform_logo_url`.


### `social_profiles_search_export_data`

This table stores the exported data for social profile searches, capturing various details about the profiles.

- **Schema**: `iiq_schema`
  - **Unique Key**: `iiq_id`
  - **Fields**:
    - `job_id`: Maps to `social_profiles_search_export_request_iiq_id`, linking the data to the request.
    - `work_platform`: Maps to platform details, including `work_platform_id`, `work_platform_name`, and `work_platform_logo_url`.
    - `platform_username`: Maps to the username on the platform.
    - `url`: Maps to the profile URL.
    - `image_url`: Maps to the profile image URL.
    - `full_name`: Maps to the full name of the profile owner.
    - `introduction`: Maps to the profile introduction or bio.
    - `is_verified`: Maps to whether the profile is verified.
    - `platform_account_type`: Maps to the type of account on the platform.
    - `gender`: Maps to the gender of the profile owner.
    - `age_group`: Maps to the age group of the profile owner.
    - `language`: Maps to the language(s) used by the profile owner.
    - `follower_count`: Maps to the number of followers.
    - `subscriber_count`: Maps to the number of subscribers.
    - `content_count`: Maps to the number of contents/posts made by the profile.
    - `engagement_rate`: Maps to the engagement rate of the profile.
    - `average_likes`: Maps to the average number of likes received by the profile.
    - `average_views`: Maps to the average number of views received by the profile.
    - `creator_location`: Maps to the location of the profile owner.
    - `contact_details`: Maps to the contact details of the profile owner.
    - `filter_match`: Maps to filter match criteria.
    - `livestream_metrics`: Maps to metrics related to live streams.

  - **Value Processors**:
    - `creator_location`: Casts the `creator_location` field to JSON format.
    - `contact_details`: Casts the `contact_details` field to JSON format.
    - `filter_match`: Casts the `filter_match` field to JSON format.
    - `livestream_metrics`: Casts the `livestream_metrics` field to JSON format.

### `social_profiles_search_export_request`

This table stores the request details for exporting social profile search data.

- **Schema**: `iiq_schema`
  - **Unique Key**: `iiq_id`
  - **Fields**:
    - `id`: Maps to `iiq_id`, which uniquely identifies the request.
    - `status`: Maps to the current status of the request.
    - `work_platform`: Maps to platform details, including `work_platform_id`, `work_platform_name`, and `work_platform_logo_url`.
    - `follower_count`: Maps to the number of followers as a filter criterion.
    - `subscriber_count`: Maps to the number of subscribers as a filter criterion.
    - `content_count`: Maps to the number of contents/posts as a filter criterion.
    - `audience_gender`: Maps to the gender of the audience.
    - `creator_gender`: Maps to the gender of the profile owner.
    - `audience_age`: Maps to the age of the audience.
    - `creator_age`: Maps to the age of the profile owner.
    - `description_keywords`: Maps to the keywords in the description as a filter criterion.
    - `is_verified`: Maps to whether the profile is verified as a filter criterion.
    - `has_contact_details`: Maps to whether the profile has contact details.
    - `specific_contact_details`: Maps to specific contact details required.
    - `last_post_timestamp`: Maps to the timestamp of the last post by the profile.
    - `audience_language`: Maps to the language(s) of the audience.
    - `creator_language`: Maps to the language(s) of the profile owner.
    - `audience_interests`: Maps to the interests of the audience.
    - `audience_interest_affinities`: Maps to the interest affinities of the audience.
    - `creator_interests`: Maps to the interests of the profile owner.
    - `audience_brand_affinities`: Maps to the brand affinities of the audience.
    - `creator_brand_affinities`: Maps to the brand affinities of the profile owner.
    - `average_likes`: Maps to the average number of likes as a filter criterion.
    - `average_views`: Maps to the average number of views as a filter criterion.
    - `engagement_rate`: Maps to the engagement rate as a filter criterion.
    - `has_sponsored_posts`: Maps to whether the profile has sponsored posts.
    - `brand_sponsors`: Maps to the brands sponsoring the profile.
    - `instagram_options`: Maps to options specific to Instagram profiles.
    - `audience_locations`: Maps to the locations of the audience.
    - `creator_locations`: Maps to the locations of the profile owner.
    - `hashtags`: Maps to hashtags used by the profile.
    - `mentions`: Maps to mentions by or of the profile.
    - `topic_relevance`: Maps to the relevance of topics to the profile.
    - `creator_age_bracket`: Maps to the age bracket of the profile owner.
    - `audience_lookalikes`: Maps to lookalike audiences.
    - `creator_lookalikes`: Maps to lookalike creators.
    - `platform_account_type`: Maps to the type of account on the platform.
    - `creator_account_type`: Maps to the type of account for the profile owner.
    - `audience_ethnicity`: Maps to the ethnicity of the audience.
    - `views_growth`: Maps to the growth in views over time.
    - `audience_source`: Maps to the source of the audience.
    - `audience_credibility_score`: Maps to the credibility score of the audience.
    - `is_official_artist`: Maps to whether the profile owner is an official artist.
    - `has_audience_info`: Maps to whether the profile has detailed audience information.
    - `share_count`: Maps to the number of shares as a filter criterion.
    - `save_count`: Maps to the number of saves as a filter criterion.
    - `exclude_private_profiles`: Maps to whether private profiles should be excluded.
    - `platform_username`: Maps to the platform username as a filter criterion.
    - `livestream_options`: Maps to options related to live streaming.

  - **Value Processors**:
    - Various fields are cast to JSON format, such as `follower_count`, `audience_age`, `audience_language`, `brand_sponsors`, etc., to handle complex data structures.
    - Fields like `exclude_private_profiles`, `has_audience_info`, `is_official_artist`, `has_sponsored_posts`, `has_contact_details`, and `is_verified` are cast to boolean values using specific value processors like `cast_string_to_bool`.

