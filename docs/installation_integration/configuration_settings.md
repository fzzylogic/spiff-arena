# Admin and Permissions

Permissions can be defined and managed at different levels such as process groups, individual processes or users. 

## Setting up Admin in Config (YAML) 

In order to initiate the creation of a process model, it is necessary to configure the terraform_deployed_environment.yml file by including at least one Admin user.

[Git Repository - Config file](https://github.com/sartography/spiff-arena/tree/main/spiffworkflow-backend/src/spiffworkflow_backend/config/permissions)

```python
groups:
  admin:
    users: [admin@spiffworkflow.org]

permissions:
  admin:
    groups: [admin]
    allowed_permissions: [create, read, update, delete]
    uri: /*
```

```{admonition} uri!
:class: info

The "uri" field defines the target resource for these permissions, which is set to "/*". This indicates that the permissions apply to all resources within the system.
```

### Groups

The "groups" section defines a group called "admin." This group is intended for users who have administrative privileges within the system.
In this example, the "admin" group consists of a single user with the associated email address. Multiple groups can be added. 

### Permissions 

The "permissions" section specifies the permissions and access control rules for the "admin" group.
The "admin" permission set allows members of the "admin" group to perform actions such as create, read, update, start and delete or all.
The "allowed_permissions" field lists the specific actions that are permitted for the "admin" group.

**Permissions allowed:**

- create

- read
  
- update
  
- delete

- start

- all
  
## Site Administration

Once the basic configuration setup is completed, specifying admin rights, you generally won't require additional permissions for designing processes and using the site. However, there might be certain situations that call for access control beyond the site or group level. In such cases, you have the flexibility to define and tailor admin requirements in a more detailed manner to fulfill specific needs.

### Step 1: Navigate to Process Groups

From the main menu select 'Procesess' and click on the 'Add a process group' button.

(how_to\suspend_a_process.md)

First create a Process Group



Describe how to create a DMN table (handled in DMN section)
Describe how to create Process flow (Can you just download it from somewhere)

Follow the structure
Remember to select Collect at the top
