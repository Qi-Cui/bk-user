# -*- coding: utf-8 -*-
"""
TencentBlueKing is pleased to support the open source community by making 蓝鲸智云-用户管理(Bk-User) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
import logging
import os

from django.db import migrations
from django.utils import timezone

from bkuser.common.constants import PERMANENT_TIME
from bkuser.common.hashers import make_password
from bkuser.plugins.base import get_default_plugin_cfg
from bkuser.plugins.constants import DataSourcePluginEnum

logger = logging.getLogger(__name__)


def forwards_func(apps, schema_editor):
    """初始化本地数据源插件"""
    admin_username = os.environ.get("INITIAL_ADMIN_USERNAME")
    admin_password = os.environ.get("INITIAL_ADMIN_PASSWORD")
    if not (admin_username and admin_password):
        raise RuntimeError("INITIAL_ADMIN_USERNAME and INITIAL_ADMIN_PASSWORD must be set in environment variables")

    logger.info("start initialize default tenant & data source with admin user [%s]...", admin_username)

    Tenant = apps.get_model("tenant", "Tenant")
    TenantUser = apps.get_model("tenant", "TenantUser")
    TenantManager = apps.get_model("tenant", "TenantManager")
    DataSource = apps.get_model("data_source", "DataSource")
    DataSourceUser = apps.get_model("data_source", "DataSourceUser")
    LocalDataSourceIdentityInfo = apps.get_model("data_source", "LocalDataSourceIdentityInfo")

    default_tenant = Tenant.objects.create(id="default", name="默认租户", is_default=True)
    data_source = DataSource.objects.create(
        name="default",
        plugin_id=DataSourcePluginEnum.LOCAL,
        owner_tenant_id=default_tenant.id,
        plugin_config=get_default_plugin_cfg(DataSourcePluginEnum.LOCAL).model_dump(),
    )

    data_source_user = DataSourceUser.objects.create(
        data_source=data_source, code=admin_username, username=admin_username, full_name=admin_username
    )
    LocalDataSourceIdentityInfo.objects.create(
        user=data_source_user,
        password=make_password(admin_password),
        password_updated_at=timezone.now(),
        password_expired_at=PERMANENT_TIME,
        data_source=data_source,
        username=admin_username,
    )
    tenant_user = TenantUser.objects.create(
        tenant=default_tenant,
        data_source_user=data_source_user,
        data_source=data_source,
        id=admin_username,
    )
    TenantManager.objects.create(tenant=default_tenant, tenant_user=tenant_user)

    logger.info("initialize default tenant & data source with admin user [%s] success", admin_username)


class Migration(migrations.Migration):
    dependencies = [
        ("tenant", "0003_auto_20231113_2017"),
        ("data_source", "0002_init_builtin_data_source_plugin"),
        ("idp", "0002_init_builtin_idp_plugin"),
    ]

    operations = [migrations.RunPython(forwards_func)]
