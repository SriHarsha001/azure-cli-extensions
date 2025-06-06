# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=line-too-long, too-many-statements, bare-except
# from azure.cli.core.commands import CliCommandType
# from azure.mgmt.core.tools import is_valid_resource_id, parse_resource_id
from azure.cli.command_modules.containerapp._transformers import (transform_containerapp_output, transform_containerapp_list_output)
from azext_containerapp._client_factory import ex_handler_factory
from ._transformers import (transform_sensitive_values,
                            transform_telemetry_data_dog_values,
                            transform_telemetry_app_insights_values,
                            transform_telemetry_otlp_values,
                            transform_telemetry_otlp_values_by_name_wrapper)
from ._utils import is_cloud_supported_by_connected_env
from ._validators import validate_debug


def load_command_table(self, args):
    with self.command_group('containerapp') as g:
        g.custom_show_command('show', 'show_containerapp', table_transformer=transform_containerapp_output)
        g.custom_command('list', 'list_containerapp', table_transformer=transform_containerapp_list_output)
        g.custom_command('create', 'create_containerapp', supports_no_wait=True, exception_handler=ex_handler_factory(), table_transformer=transform_containerapp_output, transform=transform_sensitive_values)
        g.custom_command('update', 'update_containerapp', supports_no_wait=True, exception_handler=ex_handler_factory(), table_transformer=transform_containerapp_output, transform=transform_sensitive_values)
        g.custom_command('delete', 'delete_containerapp', supports_no_wait=True, confirmation=True, exception_handler=ex_handler_factory())
        g.custom_command('up', 'containerapp_up', supports_no_wait=False, exception_handler=ex_handler_factory())
        g.custom_command('debug', 'containerapp_debug', is_preview=True, validator=validate_debug)

    with self.command_group('containerapp replica') as g:
        g.custom_show_command('show', 'get_replica')  # TODO implement the table transformer
        g.custom_command('list', 'list_replicas')
        g.custom_command('count', 'count_replicas', is_preview=True)

    with self.command_group('containerapp env') as g:
        g.custom_show_command('show', 'show_managed_environment')
        g.custom_command('list', 'list_managed_environments')
        g.custom_command('create', 'create_managed_environment', supports_no_wait=True, exception_handler=ex_handler_factory())
        g.custom_command('delete', 'delete_managed_environment', supports_no_wait=True, confirmation=True, exception_handler=ex_handler_factory())
        g.custom_command('update', 'update_managed_environment', supports_no_wait=True, exception_handler=ex_handler_factory())

    with self.command_group('containerapp env http-route-config', is_preview=True) as g:
        g.custom_show_command('show', 'show_http_route_config')
        g.custom_command('list', 'list_http_route_configs')
        g.custom_command('create', 'create_http_route_config', exception_handler=ex_handler_factory())
        g.custom_command('update', 'update_http_route_config', exception_handler=ex_handler_factory())
        g.custom_command('delete', 'delete_http_route_config', confirmation=True, exception_handler=ex_handler_factory())

    with self.command_group('containerapp job') as g:
        g.custom_show_command('show', 'show_containerappsjob')
        g.custom_command('list', 'list_containerappsjob')
        g.custom_command('create', 'create_containerappsjob', supports_no_wait=True, exception_handler=ex_handler_factory(), transform=transform_sensitive_values)
        g.custom_command('update', 'update_containerappsjob', supports_no_wait=True, exception_handler=ex_handler_factory(), transform=transform_sensitive_values)
        g.custom_command('delete', 'delete_containerappsjob', supports_no_wait=True, confirmation=True, exception_handler=ex_handler_factory())

    with self.command_group('containerapp job registry', is_preview=True) as g:
        g.custom_command('set', 'set_registry_job', exception_handler=ex_handler_factory())

    with self.command_group('containerapp env certificate') as g:
        g.custom_command('upload', 'upload_certificate')
        g.custom_command('list', 'list_certificates')
        g.custom_command('delete', 'delete_certificate', confirmation=True, exception_handler=ex_handler_factory())

    with self.command_group('containerapp env dapr-component') as g:
        g.custom_command('init', 'init_dapr_components', is_preview=True)

    with self.command_group('containerapp env identity', is_preview=True) as g:
        g.custom_command('assign', 'assign_env_managed_identity', supports_no_wait=True, exception_handler=ex_handler_factory())
        g.custom_command('remove', 'remove_env_managed_identity', supports_no_wait=True, exception_handler=ex_handler_factory())
        g.custom_show_command('show', 'show_env_managed_identity')

    with self.command_group('containerapp env storage') as g:
        g.custom_show_command('show', 'show_storage')
        g.custom_command('list', 'list_storage')
        g.custom_command('set', 'create_or_update_storage', supports_no_wait=True, exception_handler=ex_handler_factory())
        g.custom_command('remove', 'remove_storage', confirmation=True, exception_handler=ex_handler_factory())

    with self.command_group('containerapp add-on', is_preview=True) as g:
        g.custom_command('list', 'list_all_services')

    with self.command_group('containerapp add-on redis') as g:
        g.custom_command('create', 'create_redis_service', supports_no_wait=True)
        g.custom_command('delete', 'delete_redis_service', confirmation=True, supports_no_wait=True)

    with self.command_group('containerapp add-on postgres') as g:
        g.custom_command('create', 'create_postgres_service', supports_no_wait=True)
        g.custom_command('delete', 'delete_postgres_service', confirmation=True, supports_no_wait=True)

    with self.command_group('containerapp add-on kafka') as g:
        g.custom_command('create', 'create_kafka_service', supports_no_wait=True)
        g.custom_command('delete', 'delete_kafka_service', confirmation=True, supports_no_wait=True)

    with self.command_group('containerapp add-on mariadb') as g:
        g.custom_command('create', 'create_mariadb_service', supports_no_wait=True)
        g.custom_command('delete', 'delete_mariadb_service', confirmation=True, supports_no_wait=True)

    with self.command_group('containerapp add-on qdrant') as g:
        g.custom_command('create', 'create_qdrant_service', supports_no_wait=True)
        g.custom_command('delete', 'delete_qdrant_service', confirmation=True, supports_no_wait=True)

    with self.command_group('containerapp add-on weaviate') as g:
        g.custom_command('create', 'create_weaviate_service', supports_no_wait=True)
        g.custom_command('delete', 'delete_weaviate_service', confirmation=True, supports_no_wait=True)

    with self.command_group('containerapp add-on milvus') as g:
        g.custom_command('create', 'create_milvus_service', supports_no_wait=True)
        g.custom_command('delete', 'delete_milvus_service', confirmation=True, supports_no_wait=True)

    with self.command_group('containerapp registry', is_preview=True) as g:
        g.custom_command('set', 'set_registry', exception_handler=ex_handler_factory())

    with self.command_group('containerapp resiliency', is_preview=True) as g:
        g.custom_command('create', 'create_container_app_resiliency', supports_no_wait=True, exception_handler=ex_handler_factory())
        g.custom_show_command('update', 'update_container_app_resiliency', supports_no_wait=True, exception_handler=ex_handler_factory())
        g.custom_show_command('delete', 'delete_container_app_resiliency', supports_no_wait=True, confirmation=True, exception_handler=ex_handler_factory())
        g.custom_show_command('show', 'show_container_app_resiliency')
        g.custom_show_command('list', 'list_container_app_resiliencies')

    with self.command_group('containerapp env dapr-component resiliency', is_preview=True) as g:
        g.custom_command('create', 'create_dapr_component_resiliency', supports_no_wait=True, exception_handler=ex_handler_factory())
        g.custom_show_command('update', 'update_dapr_component_resiliency', supports_no_wait=True, exception_handler=ex_handler_factory())
        g.custom_show_command('delete', 'delete_dapr_component_resiliency', supports_no_wait=True, confirmation=True, exception_handler=ex_handler_factory())
        g.custom_show_command('show', 'show_dapr_component_resiliency')
        g.custom_show_command('list', 'list_dapr_component_resiliencies')

    self.command_group('containerapp env telemetry', is_preview=True)

    with self.command_group('containerapp env telemetry data-dog', is_preview=True) as g:
        g.custom_command('set', 'set_environment_telemetry_data_dog', supports_no_wait=True, exception_handler=ex_handler_factory(), transform=transform_telemetry_data_dog_values)
        g.custom_command('delete', 'delete_environment_telemetry_data_dog', supports_no_wait=True, confirmation=True, exception_handler=ex_handler_factory(), transform=transform_telemetry_data_dog_values)
        g.custom_show_command('show', 'show_environment_telemetry_data_dog', transform=transform_telemetry_data_dog_values)

    with self.command_group('containerapp env telemetry app-insights', is_preview=True) as g:
        g.custom_command('set', 'set_environment_telemetry_app_insights', supports_no_wait=True, exception_handler=ex_handler_factory(), transform=transform_telemetry_app_insights_values)
        g.custom_command('delete', 'delete_environment_telemetry_app_insights', supports_no_wait=True, confirmation=True, exception_handler=ex_handler_factory(), transform=transform_telemetry_app_insights_values)
        g.custom_show_command('show', 'show_environment_telemetry_app_insights', transform=transform_telemetry_app_insights_values)

    with self.command_group('containerapp env telemetry otlp', is_preview=True) as g:
        g.custom_command('add', 'add_environment_telemetry_otlp', supports_no_wait=True, exception_handler=ex_handler_factory(), transform=transform_telemetry_otlp_values)
        g.custom_command('update', 'update_environment_telemetry_otlp', supports_no_wait=True, exception_handler=ex_handler_factory(), transform=transform_telemetry_otlp_values)
        g.custom_command('remove', 'remove_environment_telemetry_otlp', supports_no_wait=True, confirmation=True, exception_handler=ex_handler_factory(), transform=transform_telemetry_otlp_values)
        g.custom_show_command('show', 'show_environment_telemetry_otlp', transform=transform_telemetry_otlp_values_by_name_wrapper(args))
        g.custom_show_command('list', 'list_environment_telemetry_otlp', transform=transform_telemetry_otlp_values)

    with self.command_group('containerapp github-action') as g:
        g.custom_command('add', 'create_or_update_github_action', exception_handler=ex_handler_factory())

    with self.command_group('containerapp auth') as g:
        g.custom_show_command('show', 'show_auth_config')
        g.custom_command('update', 'update_auth_config', exception_handler=ex_handler_factory())

    with self.command_group('containerapp hostname') as g:
        g.custom_command('bind', 'bind_hostname', exception_handler=ex_handler_factory())

    with self.command_group('containerapp compose') as g:
        g.custom_command('create', 'create_containerapps_from_compose')

    with self.command_group('containerapp env workload-profile') as g:
        g.custom_command('set', 'set_workload_profile', deprecate_info=self.deprecate(redirect='containerapp env workload-profile add/update', hide=True))

    with self.command_group('containerapp patch', is_preview=True) as g:
        g.custom_command('list', 'patch_list')
        g.custom_command('apply', 'patch_apply')
        g.custom_command('interactive', 'patch_interactive')

    if is_cloud_supported_by_connected_env(self.cli_ctx):
        with self.command_group('containerapp connected-env', is_preview=True) as g:
            g.custom_show_command('show', 'show_connected_environment')
            g.custom_command('list', 'list_connected_environments')
            g.custom_command('create', 'create_connected_environment', supports_no_wait=True, exception_handler=ex_handler_factory())
            g.custom_command('delete', 'delete_connected_environment', supports_no_wait=True, confirmation=True, exception_handler=ex_handler_factory())

        with self.command_group('containerapp connected-env dapr-component', is_preview=True) as g:
            g.custom_command('list', 'connected_env_list_dapr_components')
            g.custom_show_command('show', 'connected_env_show_dapr_component')
            g.custom_command('set', 'connected_env_create_or_update_dapr_component', supports_no_wait=True, exception_handler=ex_handler_factory())
            g.custom_command('remove', 'connected_env_remove_dapr_component', supports_no_wait=True, exception_handler=ex_handler_factory())

        with self.command_group('containerapp connected-env certificate', is_preview=True) as g:
            g.custom_command('list', 'connected_env_list_certificates')
            g.custom_command('upload', 'connected_env_upload_certificate', supports_no_wait=True, exception_handler=ex_handler_factory())
            g.custom_command('delete', 'connected_env_delete_certificate', supports_no_wait=True, confirmation=True, exception_handler=ex_handler_factory())

        with self.command_group('containerapp connected-env storage', is_preview=True) as g:
            g.custom_show_command('show', 'connected_env_show_storage')
            g.custom_command('list', 'connected_env_list_storages')
            g.custom_command('set', 'connected_env_create_or_update_storage', supports_no_wait=True, exception_handler=ex_handler_factory())
            g.custom_command('remove', 'connected_env_remove_storage', supports_no_wait=True, confirmation=True, exception_handler=ex_handler_factory())

    with self.command_group('containerapp arc', is_preview=True) as g:
        g.custom_command('setup-core-dns', 'setup_core_dns', confirmation=True, exception_handler=ex_handler_factory())

    with self.command_group('containerapp env java-component') as g:
        g.custom_command('list', 'list_java_components')

    with self.command_group('containerapp env java-component spring-cloud-config',
                            deprecate_info=self.deprecate(redirect='containerapp env java-component config-server-for-spring', hide=True)) as g:
        g.custom_command('create', 'create_config_server_for_spring', supports_no_wait=True)
        g.custom_command('update', 'update_config_server_for_spring', supports_no_wait=True)
        g.custom_show_command('show', 'show_config_server_for_spring')
        g.custom_command('delete', 'delete_config_server_for_spring', confirmation=True, supports_no_wait=True)

    with self.command_group('containerapp env java-component spring-cloud-eureka',
                            deprecate_info=self.deprecate(redirect='containerapp env java-component eureka-server-for-spring', hide=True)) as g:
        g.custom_command('create', 'create_eureka_server_for_spring', supports_no_wait=True)
        g.custom_command('update', 'update_eureka_server_for_spring', supports_no_wait=True)
        g.custom_show_command('show', 'show_eureka_server_for_spring')
        g.custom_command('delete', 'delete_eureka_server_for_spring', confirmation=True, supports_no_wait=True)

    with self.command_group('containerapp env java-component config-server-for-spring') as g:
        g.custom_command('create', 'create_config_server_for_spring', supports_no_wait=True)
        g.custom_command('update', 'update_config_server_for_spring', supports_no_wait=True)
        g.custom_show_command('show', 'show_config_server_for_spring')
        g.custom_command('delete', 'delete_config_server_for_spring', confirmation=True, supports_no_wait=True)

    with self.command_group('containerapp env java-component eureka-server-for-spring') as g:
        g.custom_command('create', 'create_eureka_server_for_spring', supports_no_wait=True)
        g.custom_command('update', 'update_eureka_server_for_spring', supports_no_wait=True)
        g.custom_show_command('show', 'show_eureka_server_for_spring')
        g.custom_command('delete', 'delete_eureka_server_for_spring', confirmation=True, supports_no_wait=True)

    with self.command_group('containerapp job logs', is_preview=True) as g:
        g.custom_show_command('show', 'stream_job_logs')

    with self.command_group('containerapp job replica', is_preview=True) as g:
        g.custom_show_command('list', 'list_replica_containerappsjob')

    with self.command_group('containerapp env java-component nacos', is_preview=True) as g:
        g.custom_command('create', 'create_nacos', supports_no_wait=True)
        g.custom_command('update', 'update_nacos', supports_no_wait=True)
        g.custom_show_command('show', 'show_nacos')
        g.custom_command('delete', 'delete_nacos', confirmation=True, supports_no_wait=True)

    with self.command_group('containerapp env java-component admin-for-spring') as g:
        g.custom_command('create', 'create_admin_for_spring', supports_no_wait=True)
        g.custom_command('update', 'update_admin_for_spring', supports_no_wait=True)
        g.custom_show_command('show', 'show_admin_for_spring')
        g.custom_command('delete', 'delete_admin_for_spring', confirmation=True, supports_no_wait=True)

    with self.command_group('containerapp env java-component gateway-for-spring', is_preview=True) as g:
        g.custom_command('create', 'create_gateway_for_spring', supports_no_wait=True)
        g.custom_command('update', 'update_gateway_for_spring', supports_no_wait=True)
        g.custom_show_command('show', 'show_gateway_for_spring')
        g.custom_command('delete', 'delete_gateway_for_spring', confirmation=True, supports_no_wait=True)

    with self.command_group('containerapp env dotnet-component', is_preview=True) as g:
        g.custom_command('list', 'list_dotnet_components')
        g.custom_show_command('show', 'show_dotnet_component')
        g.custom_command('create', 'create_dotnet_component', supports_no_wait=True)
        g.custom_command('delete', 'delete_dotnet_component', confirmation=True, supports_no_wait=True)

    with self.command_group('containerapp env dotnet-component', is_preview=True) as g:
        g.custom_command('list', 'list_dotnet_components')
        g.custom_show_command('show', 'show_dotnet_component')
        g.custom_command('create', 'create_dotnet_component', supports_no_wait=True)
        g.custom_command('delete', 'delete_dotnet_component', confirmation=True, supports_no_wait=True)

    with self.command_group('containerapp sessionpool') as g:
        g.custom_show_command('show', 'show_session_pool')
        g.custom_show_command('list', 'list_session_pool')
        g.custom_command('create', 'create_session_pool', supports_no_wait=True)
        g.custom_command('update', 'update_session_pool', supports_no_wait=True)
        g.custom_command('delete', 'delete_session_pool', confirmation=True, supports_no_wait=True)

    with self.command_group('containerapp session code-interpreter') as g:
        g.custom_command('execute', 'execute_session_code_interpreter', supports_no_wait=True)
        g.custom_command('upload-file', 'upload_session_code_interpreter', supports_no_wait=True)
        g.custom_show_command('show-file-content', 'show_file_content_session_code_interpreter')
        g.custom_show_command('show-file-metadata', 'show_file_metadata_session_code_interpreter')
        g.custom_show_command('list-files', 'list_files_session_code_interpreter')
        g.custom_command('delete-file', 'delete_file_session_code_interpreter', confirmation=True, supports_no_wait=True)

    with self.command_group('containerapp java logger') as g:
        g.custom_command('set', 'create_or_update_java_logger', supports_no_wait=True)
        g.custom_command('delete', 'delete_java_logger', supports_no_wait=True)
        g.custom_show_command('show', 'show_java_logger')

    with self.command_group('containerapp env maintenance-config', is_preview=True) as g:
        g.custom_command('add', 'add_maintenance_config')
        g.custom_command('update', 'update_maintenance_config')
        g.custom_command('remove', 'remove_maintenance_config', confirmation=True)
        g.custom_show_command('list', 'list_maintenance_config')

    with self.command_group('containerapp label-history', is_preview=True) as g:
        g.custom_show_command('show', 'show_label_history')
        g.custom_command('list', 'list_label_history')

    with self.command_group('containerapp revision') as g:
        g.custom_command('set-mode', 'set_revision_mode', exception_handler=ex_handler_factory())

    with self.command_group('containerapp revision label') as g:
        g.custom_command('add', 'add_revision_label')
        g.custom_command('remove', 'remove_revision_label')
