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

 