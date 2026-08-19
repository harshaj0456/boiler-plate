# Role-Based Access Control (RBAC)

Reusable RBAC implementation independent of authentication provider.

## Features

- Hierarchical roles (ADMIN > MANAGER > FIELD_WORKER > VOLUNTEER)
- Permission-based authorization
- Flexible permission system (resource.action)
- Easy integration with authentication
- Decorator-based route protection

## Architecture

```
Request
  ↓
Authentication
  ↓
Authorization
  ↓
RBAC Check (permission.check)
  ↓
YES → Controller
NO  → 403 Forbidden
```

## Permission Structure

```
Permissions: resource.action
  - project.read
  - project.create
  - project.update
  - project.delete
  - beneficiary.read
  - beneficiary.create
  - beneficiary.update
  - beneficiary.delete
  - donation.read
  - donation.create
  - donation.update

Roles:
  ADMIN
    └── * (all permissions)
  
  MANAGER
    ├── project.*
    ├── beneficiary.*
    └── donation.read
  
  FIELD_WORKER
    ├── beneficiary.read
    └── beneficiary.update
  
  VOLUNTEER
    ├── project.read
    └── task.update
```

## Usage

### FastAPI
```python
from rbac.authorization import require_permission
from fastapi import Depends

@app.delete("/projects/{project_id}")
async def delete_project(
    project_id: int,
    current_user: dict = Depends(get_current_user),
    _: None = Depends(require_permission("project.delete"))
):
    # Delete project logic
    return {"message": "Project deleted"}
```

### Flask
```python
from rbac.authorization import require_permission

@app.route("/projects/<int:project_id>", methods=["DELETE"])
@require_auth
@require_permission("project.delete")
def delete_project(current_user, project_id):
    # Delete project logic
    return {"message": "Project deleted"}
```

## Customization

Add your own roles and permissions by editing:
- `roles.py` - Define roles
- `permissions.py` - Define permissions
- `authorization.py` - Update role-permission mappings
