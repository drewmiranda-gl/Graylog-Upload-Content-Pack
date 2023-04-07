Get bundles via `/api/plugins/org.graylog.plugins.illuminate/bundles`

Get Packs in a bundle: `/api/plugins/org.graylog.plugins.illuminate/bundles/v3.2.0/packs`

```json
[
    {
      "type": "PROCESSING",
      "pack_id": "core",
      "title": "Core v3.2.0",
      "description": "Core pack",
      "enabled": false,
      "requirements": [],
      "is_core": true
    },
    {
      "type": "PROCESSING",
      "pack_id": "core_anomaly_detection",
      "title": "Illuminate v3.2.0:Core:Anomaly Detection Add-on",
      "description": "Core:Anomaly Detection Add-on technology pack. This pack is only compatible when using Graylog 4.3.0+ with the OpenSearch storage engine.",
      "enabled": true,
      "requirements": [],
      "is_core": false
    },
    {
      "type": "PROCESSING",
      "pack_id": "core-gim-enforcement",
      "title": "Illuminate Core v3.2.0:GIM Enforcement Add-on",
      "description": "Validates categorized messages meet minimum GIM field requirements. Generates the field gim_error to indicate where errors were detected and populates missing fields with default values.",
      "enabled": true,
      "requirements": [],
      "is_core": false
    },
    {
      "type": "PROCESSING",
      "pack_id": "Core:IPinfo Geolocation and AS Enrichment",
      "title": "Illuminate Core v3.2.0:Geolocation and AS Enrichment Add-on for IPinfo Databases",
      "description": "Provides Geolocation and AS enrichment for messages. Requires that the IPinfo MMDB format standard location and ASN database files, which are available from https://ipinfo.io/, are installed in /etc/graylog/server/.",
      "enabled": false,
      "requirements": [],
      "is_core": false
    },
    {
      "type": "PROCESSING",
      "pack_id": "Core:Geolocation and AS Enrichment",
      "title": "Illuminate Core v3.2.0:Geolocation and AS Enrichment Add-on for MaxMind Databases",
      "description": "Provides Geolocation and AS enrichment for messages. Requires that the MaxMind MMDB format City and ASN database files, which are available from https://www.maxmind.com/en/home, are installed in /etc/graylog/server/.",
      "enabled": true,
      "requirements": [],
      "is_core": false
    },
    {
      "type": "PROCESSING",
      "pack_id": "cbdefense-content-pack",
      "title": "Illuminate v3.2.0:Carbon Black Defense",
      "description": "Carbon Black Defense technology pack",
      "enabled": false,
      "requirements": [],
      "is_core": false
    },
    {
      "type": "PROCESSING",
      "pack_id": "ciscoasa-content-pack",
      "title": "Illuminate v3.2.0:Cisco ASA",
      "description": "Cisco ASA technology pack",
      "enabled": true,
      "requirements": [],
      "is_core": false
    },
    {
      "type": "PROCESSING",
      "pack_id": "illuminate-defender",
      "title": "Illuminate v3.2.0:Microsoft Defender",
      "description": "Microsoft Defender technology pack",
      "enabled": false,
      "requirements": [],
      "is_core": false
    },
    {
      "type": "PROCESSING",
      "pack_id": "fortigate-content-pack",
      "title": "Illuminate v3.2.0:Fortinet Fortigate",
      "description": "Fortinet Fortigate technology pack",
      "enabled": true,
      "requirements": [],
      "is_core": false
    },
    {
      "type": "PROCESSING",
      "pack_id": "illuminate-linux-auditbeat",
      "title": "Illuminate v3.2.0:Linux Auditbeat",
      "description": "Linux Auditbeat technology pack",
      "enabled": true,
      "requirements": [],
      "is_core": false
    },
    {
      "type": "PROCESSING",
      "pack_id": "meraki-content-pack",
      "title": "Illuminate v3.2.0:Cisco Meraki",
      "description": "Cisco Meraki technology pack",
      "enabled": false,
      "requirements": [],
      "is_core": false
    },
    {
      "type": "PROCESSING",
      "pack_id": "illuminate-o365",
      "title": "Illuminate v3.2.0:O365",
      "description": "Office365 technology pack",
      "enabled": true,
      "requirements": [],
      "is_core": false
    },
    {
      "type": "PROCESSING",
      "pack_id": "illuminate-okta",
      "title": "Illuminate v3.2.0:Okta",
      "description": "Okta technology pack",
      "enabled": false,
      "requirements": [],
      "is_core": false
    },
    {
      "type": "PROCESSING",
      "pack_id": "palo-alto-91x",
      "title": "Illuminate v3.2.0:Palo Alto 9.1x",
      "description": "Palo Alto 9.1x technology pack",
      "enabled": true,
      "requirements": [],
      "is_core": false
    },
    {
      "type": "PROCESSING",
      "pack_id": "illuminate-proxysg",
      "title": "Illuminate v3.2.0:Symantec ProxySG",
      "description": "Symantec ProxySG technology pack",
      "enabled": false,
      "requirements": [],
      "is_core": false
    },
    {
      "type": "PROCESSING",
      "pack_id": "illuminate-sysmon",
      "title": "Illuminate v3.2.0:Microsoft Sysmon",
      "description": "Microsoft Sysmon technology pack",
      "enabled": true,
      "requirements": [],
      "is_core": false
    },
    {
      "type": "PROCESSING",
      "pack_id": "windows-security",
      "title": "Illuminate v3.2.0:Microsoft Windows Security",
      "description": "Windows Security event log processing Technology Pack",
      "enabled": true,
      "requirements": [],
      "is_core": false
    },
    {
      "type": "PROCESSING",
      "pack_id": "e6308be4-13a0-4c02-b88b-38d83f84532d",
      "title": "Illuminate v3.2.0:SonicWall NGFW",
      "description": "This content pack will extract fields from SonicWall Next Gen Firewall event log messages and normalize fields to match the Graylog schema.",
      "enabled": false,
      "requirements": [],
      "is_core": false
    },
    {
      "type": "PROCESSING",
      "pack_id": "bb53bd77-3d3b-4f7c-a4b9-de05de837f93",
      "title": "Illuminate v3.2.0:WatchGuard Firebox",
      "description": "WatchGuard Firebox technology pack",
      "enabled": true,
      "requirements": [],
      "is_core": false
    },
    {
      "type": "PROCESSING",
      "pack_id": "cdb990e4-7dd5-457d-aea3-21cded25a0b8",
      "title": "Illuminate v3.2.0:Stormshield Firewall",
      "description": "Stormshield Firewall technology pack",
      "enabled": false,
      "requirements": [],
      "is_core": false
    },
    {
      "type": "PROCESSING",
      "pack_id": "3c5c2c47-18a5-4054-9f0e-2443f6d96d02",
      "title": "Illuminate v3.2.0:BIND DNS",
      "description": "BIND DNS technology pack\n\nThe BIND DNS pack requires:\n- Filebeat delivering logs to Graylog\n- BIND version 9\n",
      "enabled": false,
      "requirements": [],
      "is_core": false
    },
    {
      "type": "PROCESSING",
      "pack_id": "ac8ee480-3106-467e-9bcf-3c270f802158",
      "title": "Illuminate v3.2.0:Ubiquiti Unifi",
      "description": "Ubiquiti Unifi technology pack",
      "enabled": false,
      "requirements": [],
      "is_core": false
    },
    {
      "type": "PROCESSING",
      "pack_id": "symantec-endpoint-content-pack",
      "title": "Illuminate v3.2.0:Symantec Endpoint Protection",
      "description": "Symantec Endpoint Protection technology pack",
      "enabled": false,
      "requirements": [],
      "is_core": false
    },
    {
      "type": "PROCESSING",
      "pack_id": "05dc479f-9659-476b-b888-9fdaae3af85a",
      "title": "Illuminate v3.2.0:Apache HTTPD",
      "description": "Apache HTTPD technology pack",
      "enabled": false,
      "requirements": [],
      "is_core": false
    },
    {
      "type": "PROCESSING",
      "pack_id": "73788c38-0b74-4c03-8b69-2fcb4e110a9b",
      "title": "Illuminate v3.2.0:Microsoft DHCP",
      "description": "Microsoft DHCP Illuminate pack provides processing for Microsoft DHCP server event logs collected with the filebeat agent. Please review the Microsoft DHCP Illuminate pack documentation for instructions on getting Windows DHCP logs in to Graylog.\n",
      "enabled": false,
      "requirements": [],
      "is_core": false
    }
  ]
```