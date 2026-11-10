import re


SKILL_KEYWORDS = [
    "python", "java", "c++", "javascript", "sql",
    "html", "css", "react", "node.js", "flask",
    "django", "machine learning", "deep learning",
    "artificial intelligence", "data science",
    "data structures", "algorithms", "git",
    "github", "aws", "azure", "docker",
    "kubernetes", "linux", "communication",
    "problem solving", "teamwork", "leadership",
    "rest api", "mongodb", "mysql", "postgresql"
]


SKILL_FORMAT = {
    "sql": "SQL",
    "c++": "C++",
    "html": "HTML",
    "css": "CSS",
    "javascript": "JavaScript",
    "node.js": "Node.js",
    "rest api": "REST API",
    "aws": "AWS",
    "github": "GitHub",
    "mongodb": "MongoDB",
    "mysql": "MySQL",
    "postgresql": "PostgreSQL"
}


PREPARATION_TIPS = {
    "python": "Practise Python functions, OOP, collections and exception handling.",
    "java": "Practise Java OOP, collections, exception handling and coding problems.",
    "sql": "Practise SQL queries, joins, grouping and database operations.",
    "flask": "Build a small Flask application with REST API endpoints.",
    "django": "Build a Django application using models, views and database integration.",
    "javascript": "Practise JavaScript fundamentals, DOM manipulation and asynchronous programming.",
    "react": "Build a small React application using components, props and state.",
    "html": "Create accessible and well-structured web pages using semantic HTML.",
    "css": "Practise responsive layouts, Flexbox and CSS Grid.",
    "machine learning": "Study supervised learning, model evaluation and practical ML projects.",
    "artificial intelligence": "Understand AI fundamentals and build a small practical AI application.",
    "data science": "Practise data cleaning, analysis and visualization.",
    "data structures": "Practise arrays, strings, linked lists, stacks, queues and trees.",
    "algorithms": "Practise searching, sorting, recursion and time-complexity analysis.",
    "git": "Practise commits, branches, merging and resolving conflicts.",
    "github": "Maintain a GitHub repository with a clear README and documented projects.",
    "rest api": "Build and test REST API endpoints using Flask or another framework.",
    "communication": "Practise explaining technical concepts and projects clearly.",
    "problem solving": "Solve coding problems and explain your approach step by step.",
    "teamwork": "Practise collaborative development using Git and shared project tasks."
}


def format_skill(skill):
    return SKILL_FORMAT.get(skill, skill.title())


def contains_skill(text, skill):
    pattern = r'(?<!\w)' + re.escape(skill) + r'(?!\w)'
    return bool(re.search(pattern, text, re.I))


def extract_section(text, headings):
    """
    Extract text between a recognised heading and the next heading.
    """

    lines = text.splitlines()
    collecting = False
    result = []

    heading_pattern = re.compile(
        r'^\s*(?:' + "|".join(headings) + r')\s*:?\s*$',
        re.I
    )

    any_heading_pattern = re.compile(
        r'^\s*(?:about us|about the role|job overview|'
        r'responsibilities|what you will do|job duties|'
        r'requirements|qualifications|preferred qualifications|'
        r'preferred skills|desired skills|skills|required skills|'
        r'what we are looking for)\s*:?\s*$',
        re.I
    )

    for line in lines:
        clean_line = line.strip()

        if heading_pattern.match(clean_line):
            collecting = True
            continue

        if collecting and any_heading_pattern.match(clean_line):
            break

        if collecting and clean_line:
            result.append(clean_line)

    return result


def extract_bullet_items(lines):
    items = []

    for line in lines:
        item = re.sub(r'^[•\-*]\s*|\d+[.)]\s*', '', line).strip()

        if item:
            items.append(item)

    return items


def analyze_job_description(description):

    text = description.strip()
    lower_text = text.lower()

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    # 1. Role Overview

    overview = lines[0] if lines else "Job description received."

    overview = re.sub(
        r'^(job title|position|role)\s*:\s*',
        '',
        overview,
        flags=re.I
    )

    # 2. Identify required and preferred sections

    required_section = extract_section(
        text,
        ["requirements", "required skills", "qualifications"]
    )

    preferred_section = extract_section(
        text,
        ["preferred qualifications", "preferred skills", "desired skills"]
    )

    required_text = " ".join(required_section).lower()
    preferred_text = " ".join(preferred_section).lower()

    # 3. Extract skills

    required_skills = []
    preferred_skills = []

    for skill in SKILL_KEYWORDS:

        if not contains_skill(text, skill):
            continue

        if preferred_text and contains_skill(preferred_text, skill):
            preferred_skills.append(format_skill(skill))

        elif required_text and contains_skill(required_text, skill):
            required_skills.append(format_skill(skill))

        else:
            required_skills.append(format_skill(skill))

    # 4. Responsibilities

    responsibility_lines = extract_section(
        text,
        ["responsibilities", "what you will do", "job duties"]
    )

    responsibilities = extract_bullet_items(responsibility_lines)

    if not responsibilities:
        responsibilities = [
            "Review the original description for specific job duties."
        ]

    # 5. Required qualifications

    qualification_keywords = [
        "bachelor", "degree", "b.tech", "b.e.",
        "master", "m.tech", "graduate", "undergraduate",
        "certification", "experience", "qualification"
    ]

    required_qualifications = []

    for line in required_section:
        clean_line = re.sub(r'^[•\-*]\s*|\d+[.)]\s*', '', line)

        if any(keyword in clean_line.lower()
               for keyword in qualification_keywords):
            required_qualifications.append(clean_line)

    if not required_qualifications:
        required_qualifications = [
            "No explicit required qualifications identified."
        ]

    # 6. Preferred qualifications

    preferred_qualifications = []

    for line in preferred_section:
        clean_line = re.sub(r'^[•\-*]\s*|\d+[.)]\s*', '', line)

        if clean_line:
            preferred_qualifications.append(clean_line)

    if not preferred_qualifications:
        preferred_qualifications = [
            "No preferred qualifications explicitly identified."
        ]

    # 7. Preparation recommendations

    preparation_suggestions = []

    for skill in SKILL_KEYWORDS:
        if contains_skill(text, skill):
            tip = PREPARATION_TIPS.get(skill)

            if tip and tip not in preparation_suggestions:
                preparation_suggestions.append(tip)

    preparation_suggestions.extend([
        "Prepare to explain your projects and technical decisions.",
        "Practise common technical and behavioural interview questions."
    ])

    # 8. Job description quality score

    score = 0
    score_breakdown = []

    checks = [
        ("Role title", bool(overview), 15),
        ("Responsibilities", bool(responsibility_lines), 20),
        ("Required skills", bool(required_skills), 20),
        ("Qualifications", bool(required_qualifications and
                                  required_qualifications[0] !=
                                  "No explicit required qualifications identified."), 15),
        ("Preferred skills or qualifications",
         bool(preferred_skills or preferred_section), 10),
        ("Detailed description", len(text) >= 250, 10),
        ("Clear section structure", len(lines) >= 6, 10)
    ]

    for label, passed, points in checks:
        if passed:
            score += points

        score_breakdown.append({
            "criterion": label,
            "points": points if passed else 0,
            "maximum": points
        })

    if score >= 80:
        score_label = "Well-detailed description"
    elif score >= 60:
        score_label = "Moderately detailed description"
    elif score >= 40:
        score_label = "Limited job information"
    else:
        score_label = "Insufficient job information"

    return {
        "role_overview": overview,
        "required_skills": required_skills,
        "preferred_skills": preferred_skills,
        "responsibilities": responsibilities,
        "required_qualifications": required_qualifications,
        "preferred_qualifications": preferred_qualifications,
        "preparation_suggestions": preparation_suggestions,
        "quality_score": score,
        "quality_label": score_label,
        "score_breakdown": score_breakdown
    }