# github-identity-auditor
A Python tool for auditing and managing user identity links within GitHub organizations and wrapping it all up in a good looking readable table.

## Example
```
+------------------+------------------------+------------------------+
|      Login       |      SAML Name ID      |     SCIM Username      |
+------------------+------------------------+------------------------+
|      None        |    Dracula@castle.com  |          None          |
|  Frankenstein    |    Wolfman@moor.com    |          None          |
|  BrideofFrank    |   Mummy@pyramid.com    |  BrideofFrank@lab.com  |
|  FreddyKrueger   |    Jason@camp.com      |   Michael@mask.com     |
|   NormanBates    |   Chucky@dolls.com     | NormanBates@psycho.com |
+------------------+------------------------+------------------------+


```

## Usage
```
python script.py <Org Name> <Access Token>
```
