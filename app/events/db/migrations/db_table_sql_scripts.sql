CREATE SCHEMA IF NOT EXISTS iiq_schema;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
ALTER EXTENSION "uuid-ossp" SET SCHEMA pg_catalog;

CREATE TABLE IF NOT EXISTS iiq_schema.users
(
    id             UUID      DEFAULT uuid_generate_v4() NOT NULL PRIMARY KEY,
    updated_at     TIMESTAMP DEFAULT timezone('utc'::text, now()),
    created_at     TIMESTAMP DEFAULT timezone('utc'::text, now()),
    iiq_created_at TIMESTAMP WITHOUT TIME ZONE          NOT NULL,
    iiq_updated_at TIMESTAMP WITHOUT TIME ZONE          NOT NULL,
    iiq_id         UUID                                 NOT NULL,
    name           VARCHAR(100)                         NOT NULL,
    external_id    VARCHAR(100)                         NOT NULL,
    status         VARCHAR(100),
    CONSTRAINT users_iiq_id_uq UNIQUE (iiq_id)
);

ALTER TABLE iiq_schema.users
    OWNER TO iiq;

CREATE TABLE IF NOT EXISTS iiq_schema.accounts
(
    id                                    UUID      DEFAULT uuid_generate_v4() NOT NULL PRIMARY KEY,
    updated_at                            TIMESTAMP DEFAULT timezone('utc'::text, now()),
    created_at                            TIMESTAMP DEFAULT timezone('utc'::text, now()),
    iiq_id                                UUID                                 NOT NULL,
    iiq_created_at                        TIMESTAMP WITHOUT TIME ZONE          NOT NULL,
    iiq_updated_at                        TIMESTAMP WITHOUT TIME ZONE          NOT NULL,
    user_id                               UUID                                 NOT NULL,
    user_name                             VARCHAR(100)                         NOT NULL,
    work_platform_id                      UUID                                 NOT NULL,
    work_platform_name                    VARCHAR(100)                         NOT NULL,
    work_platform_logo_url                VARCHAR(2048),
    username                              VARCHAR(100),
    platform_username                     VARCHAR(100),
    profile_pic_url                       VARCHAR(1000),
    status                                VARCHAR(100)                         NOT NULL,
    platform_profile_name                 VARCHAR(100),
    platform_profile_id                   VARCHAR(100),
    platform_profile_published_at         TIMESTAMP WITHOUT TIME ZONE,
    disconnection_source                  VARCHAR(100),
    data_identity_status                  VARCHAR(100),
    data_identity_monitor_type            VARCHAR(100),
    data_identity_last_sync_at            TIMESTAMP WITHOUT TIME ZONE,
    data_identity_audience_status         VARCHAR(100),
    data_identity_audience_monitor_type   VARCHAR(100),
    data_identity_audience_last_sync_at   TIMESTAMP WITHOUT TIME ZONE,
    data_engagement_status                VARCHAR(100),
    data_engagement_monitor_type          VARCHAR(100),
    data_engagement_last_sync_at          TIMESTAMP WITHOUT TIME ZONE,
    data_engagement_refresh_since         TIMESTAMP WITHOUT TIME ZONE,
    data_engagement_data_available_from   TIMESTAMP WITHOUT TIME ZONE,
    data_engagement_audience_status       VARCHAR(100),
    data_engagement_audience_monitor_type VARCHAR(100),
    data_engagement_audience_last_sync_at TIMESTAMP WITHOUT TIME ZONE,
    data_income_status                    VARCHAR(100),
    data_income_monitor_type              VARCHAR(100),
    data_income_last_sync_at              TIMESTAMP WITHOUT TIME ZONE,
    data_income_refresh_since             TIMESTAMP WITHOUT TIME ZONE,
    data_income_data_available_from       TIMESTAMP WITHOUT TIME ZONE,
    data_activity_status                  VARCHAR(100),
    data_activity_monitor_type            TIMESTAMP WITHOUT TIME ZONE,
    data_activity_last_sync_at            VARCHAR(100),
    data_activity_refresh_since           TIMESTAMP WITHOUT TIME ZONE,
    data_activity_data_available_from     TIMESTAMP WITHOUT TIME ZONE,
    data_publish_status                   VARCHAR(100),

    CONSTRAINT accounts_iiq_id_uq UNIQUE (iiq_id)
);

ALTER TABLE iiq_schema.accounts
    OWNER TO iiq;



CREATE TABLE IF NOT EXISTS iiq_schema.profiles
(
    id                               UUID      DEFAULT uuid_generate_v4() NOT NULL PRIMARY KEY,
    updated_at                       TIMESTAMP DEFAULT timezone('utc'::text, now()),
    created_at                       TIMESTAMP DEFAULT timezone('utc'::text, now()),
    iiq_id                           UUID                                 NOT NULL,
    iiq_created_at                   TIMESTAMP WITHOUT TIME ZONE          NOT NULL,
    iiq_updated_at                   TIMESTAMP WITHOUT TIME ZONE          NOT NULL,
    user_id                          UUID                                 NOT NULL,
    user_name                        VARCHAR(100)                         NOT NULL,
    work_platform_id                 UUID                                 NOT NULL,
    work_platform_name               VARCHAR(100)                         NOT NULL,
    work_platform_logo_url           VARCHAR(2048),
    account_id                       UUID                                 NOT NULL,
    account_platform_username        VARCHAR(100),
    account_username                 VARCHAR(100)                         NOT NULL,
    username                         VARCHAR(100),
    platform_username                VARCHAR(100),
    full_name                        VARCHAR(100),
    first_name                       VARCHAR(100),
    last_name                        VARCHAR(100),
    nick_name                        VARCHAR(100),
    url                              VARCHAR(2048),
    introduction                     VARCHAR(1000),
    image_url                        VARCHAR(2048),
    date_of_birth                    DATE,
    external_id                      VARCHAR(50),
    platform_account_type            VARCHAR(50),
    category                         VARCHAR(50),
    website                          VARCHAR(2048),
    gender                           VARCHAR(100),
    country                          VARCHAR(50),
    platform_profile_name            VARCHAR(100),
    platform_profile_id              VARCHAR(100),
    platform_profile_published_at    TIMESTAMP WITHOUT TIME ZONE,
    is_verified                      BOOL,
    is_business                      BOOL,
    emails                           JSONB,
    phone_numbers                    JSONB,
    addresses                        JSONB,
    education                        JSONB,
    publications                     JSONB,
    certifications                   JSONB,
    volunteer_experiences            JSONB,
    honors                           JSONB,
    projects                         JSONB,
    work_experiences                 JSONB,
    reputation_follower_count        INTEGER,
    reputation_following_count       INTEGER,
    reputation_subscriber_count      INTEGER,
    reputation_paid_subscriber_count INTEGER,
    reputation_content_count         INTEGER,
    reputation_content_group_count   INTEGER,
    reputation_watch_time_in_hours   FLOAT,
    reputation_average_open_rate     FLOAT,
    reputation_average_click_rate    FLOAT,
    reputation_like_count            INTEGER,

    CONSTRAINT profiles_iiq_id_uq UNIQUE (iiq_id)
);
ALTER TABLE iiq_schema.profiles
    OWNER TO iiq;



CREATE TABLE IF NOT EXISTS iiq_schema.profile_audiences
(
    id                        UUID      DEFAULT uuid_generate_v4() NOT NULL PRIMARY KEY,
    updated_at                TIMESTAMP DEFAULT timezone('utc'::text, now()),
    created_at                TIMESTAMP DEFAULT timezone('utc'::text, now()),
    iiq_id                    UUID                                 NOT NULL,
    iiq_created_at            TIMESTAMP WITHOUT TIME ZONE          NOT NULL,
    iiq_updated_at            TIMESTAMP WITHOUT TIME ZONE          NOT NULL,
    user_id                   UUID                                 NOT NULL,
    user_name                 VARCHAR(100)                         NOT NULL,
    work_platform_id          UUID                                 NOT NULL,
    work_platform_name        VARCHAR(100)                         NOT NULL,
    work_platform_logo_url    VARCHAR(2048),
    account_id                UUID                                 NOT NULL,
    account_platform_username VARCHAR(100),
    account_username          VARCHAR(100)                         NOT NULL,
    countries                 JSONB,
    cities                    JSONB,
    gender_age_distribution   JSONB,

    CONSTRAINT profile_audiences_iiq_id_uq UNIQUE (iiq_id)
);
ALTER TABLE iiq_schema.profile_audiences
    OWNER TO iiq;



CREATE TABLE IF NOT EXISTS iiq_schema.contents
(
    id                                  UUID      DEFAULT uuid_generate_v4() NOT NULL PRIMARY KEY,
    updated_at                          TIMESTAMP DEFAULT timezone('utc'::text, now()),
    created_at                          TIMESTAMP DEFAULT timezone('utc'::text, now()),
    iiq_id                              UUID                                 NOT NULL,
    iiq_created_at                      TIMESTAMP WITHOUT TIME ZONE          NOT NULL,
    iiq_updated_at                      TIMESTAMP WITHOUT TIME ZONE          NOT NULL,
    user_id                             UUID                                 NOT NULL,
    user_name                           VARCHAR(100)                         NOT NULL,
    work_platform_id                    UUID                                 NOT NULL,
    work_platform_name                  VARCHAR(100)                         NOT NULL,
    work_platform_logo_url              VARCHAR(2048),
    account_id                          UUID                                 NOT NULL,
    account_platform_username           VARCHAR(100),
    account_username                    VARCHAR(100)                         NOT NULL,
    engagement_like_count               INTEGER,
    engagement_dislike_count            INTEGER,
    engagement_comment_count            INTEGER,
    engagement_impression_organic_count INTEGER,
    engagement_reach_organic_count      INTEGER,
    engagement_save_count               INTEGER,
    engagement_view_count               INTEGER,
    engagement_watch_time_in_hours      FLOAT,
    engagement_share_count              INTEGER,
    engagement_impression_paid_count    INTEGER,
    engagement_reach_paid_count         INTEGER,
    engagement_email_open_rate          FLOAT,
    engagement_email_click_rate         FLOAT,
    engagement_unsubscribe_count        INTEGER,
    engagement_spam_report_count        INTEGER,
    engagement_click_count              INTEGER,
    engagement_additional_info          JSONB,
    authors                             VARCHAR(100)[],
    audience                            VARCHAR(100),
    platform                            VARCHAR(100),
    external_id                         VARCHAR(50)                          NOT NULL,
    title                               VARCHAR(5000),
    format                              VARCHAR(100)                         NOT NULL,
    type                                VARCHAR(100)                         NOT NULL,
    url                                 VARCHAR(2048),
    media_url                           VARCHAR(2048),
    duration                            INTEGER,
    description                         VARCHAR(5000),
    visibility                          VARCHAR(100)                         NOT NULL,
    thumbnail_url                       VARCHAR(2048),
    persistent_thumbnail_url            VARCHAR(2048),
    published_at                        TIMESTAMP WITHOUT TIME ZONE,
    platform_profile_id                 VARCHAR(100),
    platform_profile_name               VARCHAR(100),
    is_owned_by_platform_user           BOOL,
    hashtags                            VARCHAR(500)[],
    content_tags                        VARCHAR(500)[],
    mentions                            VARCHAR(500)[],
    media_urls                          JSONB,
    sponsored_is_sponsored              BOOL,
    sponsored_tags                      VARCHAR(500)[],
    collaboration_has_collaborators     BOOL,

    CONSTRAINT contents_iiq_id_uq UNIQUE (iiq_id)
);
ALTER TABLE iiq_schema.contents
    OWNER TO iiq;



CREATE TABLE IF NOT EXISTS iiq_schema.content_groups
(
    id                                  UUID      DEFAULT uuid_generate_v4() NOT NULL PRIMARY KEY,
    updated_at                          TIMESTAMP DEFAULT timezone('utc'::text, now()),
    created_at                          TIMESTAMP DEFAULT timezone('utc'::text, now()),
    iiq_id                              UUID                                 NOT NULL,
    iiq_created_at                      TIMESTAMP WITHOUT TIME ZONE          NOT NULL,
    iiq_updated_at                      TIMESTAMP WITHOUT TIME ZONE          NOT NULL,
    user_id                             UUID                                 NOT NULL,
    user_name                           VARCHAR(100)                         NOT NULL,
    work_platform_id                    UUID                                 NOT NULL,
    work_platform_name                  VARCHAR(100)                         NOT NULL,
    work_platform_logo_url              VARCHAR(2048),
    account_id                          UUID                                 NOT NULL,
    account_platform_username           VARCHAR(100),
    account_username                    VARCHAR(100)                         NOT NULL,

    engagement_like_count               INTEGER,
    engagement_dislike_count            INTEGER,
    engagement_comment_count            INTEGER,
    engagement_impression_organic_count INTEGER,
    engagement_reach_organic_count      INTEGER,
    engagement_save_count               INTEGER,
    engagement_view_count               INTEGER,
    engagement_watch_time_in_hours      FLOAT,
    engagement_share_count              INTEGER,
    engagement_impression_paid_count    INTEGER,
    engagement_reach_paid_count         INTEGER,
    external_id                         VARCHAR(50)                          NOT NULL,
    title                               VARCHAR(5000),
    format                              VARCHAR(100)                         NOT NULL,
    type                                VARCHAR(100)                         NOT NULL,
    url                                 VARCHAR(2048),
    description                         VARCHAR(5000),
    visibility                          VARCHAR(100)                         NOT NULL,
    thumbnail_url                       VARCHAR(2048),
    media_url                           VARCHAR(2048),
    persistent_thumbnail_url            VARCHAR(2048),
    published_at                        TIMESTAMP WITHOUT TIME ZONE,
    platform_profile_id                 VARCHAR(100),
    platform_profile_name               VARCHAR(100),
    item_count                          INTEGER,
    hashtags                            VARCHAR(500)[],
    CONSTRAINT content_groups_iiq_id_uq UNIQUE (iiq_id)
);
ALTER TABLE iiq_schema.content_groups
    OWNER TO iiq;



CREATE TABLE IF NOT EXISTS iiq_schema.social_transactions
(
    id                        UUID      DEFAULT uuid_generate_v4() NOT NULL PRIMARY KEY,
    updated_at                TIMESTAMP DEFAULT timezone('utc'::text, now()),
    created_at                TIMESTAMP DEFAULT timezone('utc'::text, now()),
    iiq_id                    UUID                                 NOT NULL,
    iiq_created_at            TIMESTAMP WITHOUT TIME ZONE          NOT NULL,
    iiq_updated_at            TIMESTAMP WITHOUT TIME ZONE          NOT NULL,
    user_id                   UUID                                 NOT NULL,
    user_name                 VARCHAR(100)                         NOT NULL,
    work_platform_id          UUID                                 NOT NULL,
    work_platform_name        VARCHAR(100)                         NOT NULL,
    work_platform_logo_url    VARCHAR(2048),
    account_id                UUID                                 NOT NULL,
    account_platform_username VARCHAR(100),
    account_username          VARCHAR(100)                         NOT NULL,

    amount                    FLOAT,
    type                      VARCHAR(100),
    cpm                       FLOAT,
    currency                  VARCHAR(50),
    external_id               VARCHAR(100),
    transaction_at            TIMESTAMP WITHOUT TIME ZONE,
    platform_profile_id       VARCHAR(100),
    platform_profile_name     VARCHAR(100),
    CONSTRAINT social_transactions_iiq_id_uq UNIQUE (iiq_id)
);
ALTER TABLE iiq_schema.social_transactions
    OWNER TO iiq;



CREATE TABLE IF NOT EXISTS iiq_schema.social_payouts
(
    id                                  UUID      DEFAULT uuid_generate_v4() NOT NULL PRIMARY KEY,
    updated_at                          TIMESTAMP DEFAULT timezone('utc'::text, now()),
    created_at                          TIMESTAMP DEFAULT timezone('utc'::text, now()),
    iiq_id                              UUID                                 NOT NULL,
    iiq_created_at                      TIMESTAMP WITHOUT TIME ZONE          NOT NULL,
    iiq_updated_at                      TIMESTAMP WITHOUT TIME ZONE          NOT NULL,
    user_id                             UUID                                 NOT NULL,
    user_name                           VARCHAR(100)                         NOT NULL,
    work_platform_id                    UUID                                 NOT NULL,
    work_platform_name                  VARCHAR(100)                         NOT NULL,
    work_platform_logo_url              VARCHAR(2048),
    account_id                          UUID                                 NOT NULL,
    account_platform_username           VARCHAR(100),
    account_username                    VARCHAR(100)                         NOT NULL,
    external_id                         VARCHAR(100),
    amount                              FLOAT,
    currency                            VARCHAR(50),
    type                                VARCHAR(100),
    status                              VARCHAR(100),
    payout_interval                     VARCHAR(100),
    bank_details_name                   VARCHAR(100),
    bank_details_account_last_digits    VARCHAR(100),
    bank_details_account_routing_number VARCHAR(100),
    payout_at                           TIMESTAMP WITHOUT TIME ZONE,
    platform_profile_id                 VARCHAR(100),
    platform_profile_name               VARCHAR(100),
    CONSTRAINT social_payouts_iiq_id_uq UNIQUE (iiq_id)
);
ALTER TABLE iiq_schema.social_payouts
    OWNER TO iiq;



CREATE TABLE IF NOT EXISTS iiq_schema.activity_artists
(
    id                        UUID      DEFAULT uuid_generate_v4() NOT NULL PRIMARY KEY,
    updated_at                TIMESTAMP DEFAULT timezone('utc'::text, now()),
    created_at                TIMESTAMP DEFAULT timezone('utc'::text, now()),
    iiq_id                    UUID                                 NOT NULL,
    iiq_created_at            TIMESTAMP WITHOUT TIME ZONE          NOT NULL,
    iiq_updated_at            TIMESTAMP WITHOUT TIME ZONE          NOT NULL,
    user_id                   UUID                                 NOT NULL,
    user_name                 VARCHAR(100)                         NOT NULL,
    work_platform_id          UUID                                 NOT NULL,
    work_platform_name        VARCHAR(100)                         NOT NULL,
    work_platform_logo_url    VARCHAR(2048),
    account_id                UUID                                 NOT NULL,
    account_platform_username VARCHAR(100),
    account_username          VARCHAR(100)                         NOT NULL,

    platform_artist_id        VARCHAR(256)                         NOT NULL,
    image_url                 VARCHAR(2048),
    artist_name               VARCHAR(100)                         NOT NULL,
    artist_url                VARCHAR(2048),
    genre                     VARCHAR(50)[],
    activity_type             VARCHAR(100)                         NOT NULL,

    CONSTRAINT activity_artists_iiq_id_uq UNIQUE (iiq_id)
);
ALTER TABLE iiq_schema.activity_artists
    OWNER TO iiq;


CREATE TABLE IF NOT EXISTS iiq_schema.activity_contents
(
    id                        UUID      DEFAULT uuid_generate_v4() NOT NULL PRIMARY KEY,
    updated_at                TIMESTAMP DEFAULT timezone('utc'::text, now()),
    created_at                TIMESTAMP DEFAULT timezone('utc'::text, now()),
    iiq_id                    UUID                                 NOT NULL,
    iiq_created_at            TIMESTAMP WITHOUT TIME ZONE          NOT NULL,
    iiq_updated_at            TIMESTAMP WITHOUT TIME ZONE          NOT NULL,
    user_id                   UUID                                 NOT NULL,
    user_name                 VARCHAR(100)                         NOT NULL,
    work_platform_id          UUID                                 NOT NULL,
    work_platform_name        VARCHAR(100)                         NOT NULL,
    work_platform_logo_url    VARCHAR(2048),
    account_id                UUID                                 NOT NULL,
    account_platform_username VARCHAR(100),
    account_username          VARCHAR(100)                         NOT NULL,
    platform_content_id       VARCHAR(50)                          NOT NULL,
    title                     VARCHAR(5000),
    format                    VARCHAR(100)                         NOT NULL,
    type                      VARCHAR(100)                         NOT NULL,
    url                       VARCHAR(2048)                        NOT NULL,
    description               VARCHAR(5000),
    thumbnail_url             VARCHAR(2048),
    embed_url                 VARCHAR(2048),
    activity_type             VARCHAR(100),
    additional_info_artists   VARCHAR(256)[],
    additional_info_album     VARCHAR(500),
    additional_info_genre     VARCHAR(50)[],


    CONSTRAINT activity_contents_iiq_id_uq UNIQUE (iiq_id)
);
ALTER TABLE iiq_schema.activity_contents
    OWNER TO iiq;



CREATE TABLE IF NOT EXISTS iiq_schema.publish_contents
(
    id                                 UUID      DEFAULT uuid_generate_v4() NOT NULL PRIMARY KEY,
    updated_at                         TIMESTAMP DEFAULT timezone('utc'::text, now()),
    created_at                         TIMESTAMP DEFAULT timezone('utc'::text, now()),
    iiq_id                             UUID                                 NOT NULL,
    iiq_created_at                     TIMESTAMP WITHOUT TIME ZONE          NOT NULL,
    iiq_updated_at                     TIMESTAMP WITHOUT TIME ZONE          NOT NULL,
    user_id                            UUID                                 NOT NULL,
    user_name                          VARCHAR(100)                         NOT NULL,
    work_platform_id                   UUID                                 NOT NULL,
    work_platform_name                 VARCHAR(100)                         NOT NULL,
    work_platform_logo_url             VARCHAR(2048),
    account_id                         UUID                                 NOT NULL,
    account_platform_username          VARCHAR(100),
    account_username                   VARCHAR(100)                         NOT NULL,

    status                             VARCHAR(100)                         NOT NULL,
    title                              VARCHAR(5000),
    type                               VARCHAR(100)                         NOT NULL,
    format                             VARCHAR(100)                         NOT NULL,
    description                        VARCHAR(5000),
    visibility                         VARCHAR(100),
    retry                              BOOL,
    additional_info_share_to_feed      BOOL,
    media                              JSONB,
    published_info_content_id          UUID,
    published_info_url                 VARCHAR(2048),
    published_info_media_url           VARCHAR(2048),
    published_info_thumbnail_url       VARCHAR(2048),
    published_info_published_at        TIMESTAMP WITHOUT TIME ZONE,
    published_info_platform_content_id VARCHAR(100),


    CONSTRAINT publish_contents_iiq_id_uq UNIQUE (iiq_id)
);
ALTER TABLE iiq_schema.publish_contents
    OWNER TO iiq;



CREATE TABLE IF NOT EXISTS iiq_schema.basic_profile_info
(
    id                     UUID      DEFAULT uuid_generate_v4() NOT NULL PRIMARY KEY,
    updated_at             TIMESTAMP DEFAULT timezone('utc'::text, now()),
    created_at             TIMESTAMP DEFAULT timezone('utc'::text, now()),
    work_platform_id       UUID                                 NOT NULL,
    work_platform_name     VARCHAR(100)                         NOT NULL,
    work_platform_logo_url VARCHAR(2048),
    platform_username      VARCHAR(500)                         NOT NULL,
    url                    VARCHAR(2048)                        NOT NULL,
    image_url              VARCHAR(2048),
    full_name              VARCHAR(500),
    follower_count         INTEGER,
    following_count        INTEGER,
    subscriber_count       INTEGER,
    is_verified            BOOL,
    is_business            BOOL,
    is_private             BOOL,
    content_count          INTEGER,
    total_view_count       INTEGER,
    introduction           VARCHAR(5000),
    category               VARCHAR(100),
    profile_links          JSONB,
    platform_profile_id    VARCHAR(200)                         NOT NULL,
    external_id            VARCHAR(200)                         NOT NULL,
    CONSTRAINT basic_profile_info_wpid_external_id UNIQUE (work_platform_id, external_id)
);
ALTER TABLE iiq_schema.basic_profile_info
    OWNER TO iiq;