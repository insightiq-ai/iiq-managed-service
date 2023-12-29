from app.utils.mapping_utils import get_mapping_config_from_yaml_file
import os

current_dir = os.path.dirname(__file__)
mapping_file_path = 'db_table_field_mappings.yaml'
mapper_config_file_path = os.path.join(current_dir, mapping_file_path)
config = get_mapping_config_from_yaml_file(mapper_config_file_path)

USER_TABLE_MAPPINGS = config.get('mappings', {}).get('user', {})
ACCOUNT_TABLE_MAPPINGS = config.get('mappings', {}).get('account', {})
PROFILE_TABLE_MAPPINGS = config.get('mappings', {}).get('profile', {})
PROFILE_AUDIENCE_TABLE_MAPPINGS = config.get('mappings', {}).get('profile_audience', {})
CONTENT_TABLE_MAPPINGS = config.get('mappings', {}).get('content', {})
CONTENT_COMMENT_TABLE_MAPPINGS = config.get('mappings', {}).get('content_comment', {})
CONTENT_GROUP_TABLE_MAPPINGS = config.get('mappings', {}).get('content_group', {})
SOCIAL_TRANSACTION_TABLE_MAPPINGS = config.get('mappings', {}).get('social_transaction', {})
COMMERCE_TRANSACTION_TABLE_MAPPINGS = config.get('mappings', {}).get('commerce_transaction', {})
SOCIAL_PAYOUT_TABLE_MAPPINGS = config.get('mappings', {}).get('social_payout', {})
COMMERCE_PAYOUT_TABLE_MAPPINGS = config.get('mappings', {}).get('commerce_payout', {})
COMMERCE_BALANCE_TABLE_MAPPINGS = config.get('mappings', {}).get('commerce_balance', {})
ACTIVITY_ARTISTS_TABLE_MAPPINGS = config.get('mappings', {}).get('activity_artist', {})
ACTIVITY_CONTENTS_TABLE_MAPPINGS = config.get('mappings', {}).get('activity_content', {})
PROFILE_FETCH_TABLE_MAPPINGS = config.get('mappings', {}).get('profile_fetch', {})
PROFILE_SEARCH_TABLE_MAPPINGS = config.get('mappings', {}).get('profile_search', {})
PROFILE_ANALYTICS_TABLE_MAPPINGS = config.get('mappings', {}).get('profile_analytics', {})
CONTENTS_INFORMATION_TABLE_MAPPINGS = config.get('mappings', {}).get('contents_information', {})
PUBLISH_CONTENT_TABLE_MAPPINGS = config.get('mappings', {}).get('publish_content', {})
