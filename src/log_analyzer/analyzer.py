def summarize_events(events, blueprint):
    summary = {"log_summary": []}
    severity_rules = blueprint.get("severity_keywords", {})
    category_rules = blueprint.get("category_rules", {})
    default_category = blueprint.get("default_category", "system")
    
    severity_priority = ['ERROR', 'WARNING', 'INFO', 'DEBUG']  # high → low

    for event in events:
        line = event['raw'].lower()

        # Detect severity
        severity = 'INFO'
        for level in severity_priority:
            keywords = severity_rules.get(level, [])
            if any(kw.lower() in line for kw in keywords):
                severity = level
                break

        # Detect category
        category = default_category
        for cat, keywords in category_rules.items():
            if any(kw.lower() in line for kw in keywords):
                category = cat
                break

        summary["log_summary"].append({
            "message": event["raw"],
            "severity": severity,
            "category": category
        })

    return summary