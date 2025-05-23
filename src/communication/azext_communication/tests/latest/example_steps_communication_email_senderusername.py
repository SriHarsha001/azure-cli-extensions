# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------


from .. import try_manual


# EXAMPLE: /SenderUsername/put/Create or update resource
@try_manual
def step_create(test, rg, ecs, domain, checks=None):
    if checks is None:
        checks = []
    test.cmd('az communication email domain sender-username create '
             '--sender-username "{mySenderUsername}" '
             '--domain-name "{domain}" '
             '--email-service-name "{ecs}" '
             '--username "{mySenderUsername}" '
             '--resource-group "{rg}"',
             checks=checks)


# EXAMPLE: /SenderUsername/get/Get resource
@try_manual
def step_show(test, rg, ecs, domain, checks=None):
    if checks is None:
        checks = []
    test.cmd('az communication email domain sender-username show '
             '--sender-username "{mySenderUsername}" '
             '--domain-name "{domain}" '
             '--email-service-name "{ecs}" '
             '--resource-group "{rg}"',
             checks=checks)


# EXAMPLE: /SenderUsername/get/List by domain
@try_manual
def step_list(test, rg, ecs, domain, checks=None):
    if checks is None:
        checks = []
    test.cmd('az communication email domain sender-username list '
             '--domain-name "{domain}" '
             '--email-service-name "{ecs}" '
             '--resource-group "{rg}"',
             checks=checks)


# EXAMPLE: /SenderUsername/get/List by domain with alternative resource group command
@try_manual
def step_list2(test, rg, ecs, domain, checks=None):
    if checks is None:
        checks = []
    test.cmd('az communication email domain sender-username list '
             '--domain-name "{domain}" '
             '--email-service-name "{ecs}" '
             '-g "{rg}"',
             checks=checks)


# EXAMPLE: /SenderUsername/patch/Update resource
@try_manual
def step_update(test, rg, ecs, domain, checks=None):
    if checks is None:
        checks = []
    test.cmd('az communication email domain sender-username update '
             '--sender-username "{mySenderUsername}" '
             '--domain-name "{domain}" '
             '--email-service-name "{ecs}" '
             '--display-name "newDisplayname" '
             '--resource-group "{rg}"',
             checks=checks)

# EXAMPLE: /SenderUsername/delete/Delete resource
@try_manual
def step_delete(test, rg, ecs, domain, checks=None):
    if checks is None:
        checks = []
    test.cmd('az communication email domain sender-username delete -y '
             '--sender-username "{mySenderUsername}" '
             '--domain-name "{domain}" '
             '--email-service-name "{ecs}" '
             '--resource-group "{rg}"',
             checks=checks)
