DEMO_JD = """
Senior Backend Engineer at Acme Corp

About the role:
We are looking for a Senior Backend Engineer to join our platform team in Sydney.
You will design and build APIs that power our core product, work closely with
frontend engineers, and help scale our infrastructure to support millions of users.

Requirements:
- 5+ years of experience with Python
- Strong knowledge of FastAPI or Django REST Framework
- Experience with PostgreSQL and Redis
- Familiarity with Docker and Kubernetes
- Understanding of CI/CD pipelines (GitHub Actions, CircleCI)
- Experience designing RESTful and GraphQL APIs

Nice to have:
- Experience with event-driven architecture (Kafka, RabbitMQ)
- Familiarity with Terraform or Pulumi for infrastructure as code
- Contributions to open source projects
- Experience mentoring junior developers

About you:
- You communicate clearly in writing and in person
- You care about code quality but know when to ship
- You are comfortable working in a fast-paced startup environment

Salary: $160,000 - $200,000 AUD + equity
Location: Sydney, Australia (hybrid, 3 days in office)
Visa sponsorship: Not available
""".strip()

DEMO_CV = """
Olavo Silverio, Python Developer and Creative Technologist based in Sydney.

Experience:
- 3 years building Python applications (FastAPI, Flask, automation scripts)
- 2 years developing interactive experiences with Unity and C#
- Built internal tools and data pipelines for media production workflows
- Automated repetitive tasks saving 15+ hours per week across teams
- Deployed containerized applications using Docker on AWS

Skills: Python, FastAPI, Flask, C#, Unity, Docker, PostgreSQL, Git,
JavaScript, HTML/CSS, REST APIs, automation, scripting, data processing

Education: Bachelor of IT (expected 2025), currently on student visa
working up to 48 hours per fortnight.

Projects:
- Job Intel Agent: AI-powered tool that analyzes job descriptions and
  scores CV fit using the Claude API
- Automation suite for video production pipeline (Python + FFmpeg)
- Portfolio website with interactive 3D elements (Three.js + Unity WebGL)

Looking for backend or full-stack roles where I can combine my Python
skills with creative problem-solving. Open to contract or part-time
positions that fit within visa work limits.
""".strip()

DEMO_SCORE = {
    "match_percentage": 52,
    "gap_list": [
        "Requires 5+ years Python experience (you have 3)",
        "No demonstrated Redis experience",
        "No Kubernetes experience listed",
        "CI/CD pipeline experience not mentioned",
        "GraphQL API experience not listed",
        "Visa sponsorship not available (you require sponsorship)",
    ],
    "talking_points": [
        "Direct FastAPI experience matches their primary framework requirement",
        "Docker deployment experience aligns with their containerization needs",
        "PostgreSQL listed in your skills matches their database stack",
        "Automation background shows ability to improve team productivity",
    ],
    "pitch": "I bring hands-on FastAPI and PostgreSQL experience that directly "
    "maps to your stack, plus a track record of building automation that "
    "saves teams real time. My background combining Python backend work "
    "with creative technology gives me a practical, ship-oriented mindset. "
    "I would love to discuss how my experience building APIs and internal "
    "tools fits your platform team's needs.",
}

DEMO_REWRITE = {
    "tips": [
        {
            "section": "Experience",
            "problem": "Years of experience listed as 3, but the role asks for 5+",
            "suggestion": "Lead with total years in tech (including Unity/C#) to show breadth, then specify Python depth separately",
        },
        {
            "section": "Skills",
            "problem": "Redis, Kubernetes, and CI/CD are missing from your skills list",
            "suggestion": "If you have any exposure to these (even tutorials or side projects), add them with honest framing like 'familiar with' rather than omitting entirely",
        },
        {
            "section": "Projects",
            "problem": "Projects don't demonstrate API scale or infrastructure work",
            "suggestion": "Add metrics where possible: request volume, data size, uptime. Mention Docker deployment details (orchestration, monitoring)",
        },
        {
            "section": "Summary",
            "problem": "Opening line does not target backend engineering specifically",
            "suggestion": "Rewrite the summary to lead with backend/API experience and mention the exact stack they use (FastAPI, PostgreSQL, Docker)",
        },
    ],
    "rewritten_cv": (
        "Olavo Silverio\n"
        "Backend Developer, Sydney\n\n"
        "Summary:\n"
        "Backend developer with 3 years of Python experience building APIs and "
        "automation tools using FastAPI, Flask, and PostgreSQL. 5 years total in "
        "software development including interactive applications with Unity/C#. "
        "Proven track record of shipping containerized applications on AWS with Docker.\n\n"
        "Technical Skills:\n"
        "Languages: Python, C#, JavaScript, SQL\n"
        "Frameworks: FastAPI, Flask, REST APIs\n"
        "Infrastructure: Docker, PostgreSQL, AWS, Git\n"
        "Other: Automation, Data Processing, HTML/CSS\n\n"
        "Experience:\n"
        "- Built and maintained Python APIs using FastAPI serving production traffic\n"
        "- Designed data pipelines and internal tools for media production workflows\n"
        "- Automated manual processes, saving 15+ hours per week across teams\n"
        "- Deployed and managed containerized applications using Docker on AWS\n"
        "- Developed interactive experiences with Unity and C# over 2 years\n\n"
        "Projects:\n"
        "- Job Intel Agent: Full-stack tool (FastAPI + Claude API) that analyzes "
        "job descriptions and scores CV fit using structured output\n"
        "- Video Production Automation: Python + FFmpeg pipeline handling batch "
        "media processing\n"
        "- Portfolio Site: Three.js + Unity WebGL interactive web application\n\n"
        "Education:\n"
        "Bachelor of IT (expected 2025)\n"
        "Available up to 48 hours per fortnight (student visa)"
    ),
}
