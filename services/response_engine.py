def generate_response(user_text, conversation_history=None):

    question = user_text.lower().strip()
    history = conversation_history or []

    # Get previous conversation
    previous_user = ""
    previous_response = ""

    if history:
        previous_user = history[-1].get("user", "").lower()
        previous_response = history[-1].get("assistant", "").lower()

    # 1. Greetings
    if question in ["hi", "hello", "hey", "hii", "good morning"]:
        return (
            "Hello! Welcome to VoxPath AI. "
            "I'm here to help you build your software career. "
            "We can explore programming, projects, internships, "
            "interviews, and career roadmaps. What would you "
            "like to work on today?"
        )

    # 2. Context-aware follow-up questions
    follow_ups = [
        "tell me more", "explain more", "which one",
        "which is best", "why", "how about that",
        "the first one", "the second one",
        "that one", "what about it"
    ]

    if any(phrase in question for phrase in follow_ups):

        if "project" in previous_user or "project" in previous_response:
            return (
                "Let's explore that project further. Start by defining "
                "the problem it solves. Then identify the technologies, "
                "design the database, develop the main features, and "
                "test the application. Finally, document it on GitHub."
            )

        if "internship" in previous_user or "internship" in previous_response:
            return (
                "For internship preparation, concentrate on three areas: "
                "programming fundamentals, problem-solving, and practical "
                "projects. Prepare your resume and practice explaining "
                "your technical work clearly."
            )

        if "resume" in previous_user or "resume" in previous_response:
            return (
                "Let's improve your resume step by step. Start with "
                "your education, technical skills, and two or three "
                "strong projects. Explain the problem, technologies "
                "used, and your contribution to each project."
            )

        return (
            "Could you tell me which part you want to explore further? "
            "I can explain programming, projects, internships, "
            "career options, or interview preparation."
        )

    # 3. Career guidance
    if any(word in question for word in [
        "career", "career path", "career options", "software engineer"
    ]):
        return (
            "A software engineering career can involve backend "
            "development, frontend development, full-stack engineering, "
            "AI and machine learning, or cloud computing. "
            "Start by strengthening programming and DSA. Build "
            "practical projects and explore different roles before "
            "choosing a specialization."
        )

    # 4. Project recommendations
    if any(word in question for word in [
        "project", "projects", "portfolio"
    ]):

        if "python" in question:
            return (
                "Here are five Python project ideas:\n\n"
                "1. Student Management System - Python and SQLite.\n\n"
                "2. Smart Expense Tracker - Flask and SQLite.\n\n"
                "3. AI Career Assistant - Career guidance application.\n\n"
                "4. Weather Forecast Application - Weather API integration.\n\n"
                "5. Smart Complaint Management System - Flask and SQLite.\n\n"
                "Choose a project based on your current skills and "
                "gradually add more advanced features."
            )

        return (
            "Here are some portfolio project ideas:\n\n"
            "1. AI Career Guidance Platform.\n"
            "2. Smart Expense Tracker.\n"
            "3. Student Management System.\n"
            "4. Online Learning Platform.\n"
            "5. Smart Complaint Management System.\n\n"
            "Choose one that solves a real problem and demonstrates "
            "your programming, database, and development skills."
        )

    # 5. Internship guidance
    elif any(word in question for word in [
        "internship", "intern", "work experience"
    ]):
        return (
            "To prepare for software internships, follow these steps:\n\n"
            "1. Strengthen C++, Python, or Java fundamentals.\n"
            "2. Practice Data Structures and Algorithms.\n"
            "3. Build two or three practical projects.\n"
            "4. Maintain a professional GitHub profile.\n"
            "5. Prepare a clear technical resume.\n"
            "6. Apply to suitable internship opportunities.\n\n"
            "Also practice explaining your projects and technical "
            "decisions during interviews."
        )

    # 6. Interview preparation
    elif any(word in question for word in [
        "interview", "mock interview", "technical round"
    ]):
        return (
            "Your software interview preparation should cover:\n\n"
            "1. Programming fundamentals.\n"
            "2. Data Structures and Algorithms.\n"
            "3. Object-Oriented Programming.\n"
            "4. Database Management Systems.\n"
            "5. Operating Systems.\n"
            "6. Computer Networks.\n"
            "7. Project explanation.\n\n"
            "Practice coding problems and explain your approach "
            "clearly before writing the solution."
        )

    # 7. Resume and GitHub guidance
    elif any(word in question for word in [
        "resume", "cv", "github", "linkedin"
    ]):
        return (
            "A professional software engineering resume should include:\n\n"
            "1. Education and academic achievements.\n"
            "2. Programming and technical skills.\n"
            "3. Practical projects with technologies used.\n"
            "4. Internships and relevant experience.\n"
            "5. Certifications and achievements.\n\n"
            "Keep your GitHub repositories organized with meaningful "
            "README files, project descriptions, and clear documentation."
        )

    # 8. Learning roadmap
    elif any(word in question for word in [
        "roadmap", "learning path", "where should i start"
    ]):
        return (
            "Here is a beginner-friendly software development roadmap:\n\n"
            "Stage 1: Learn programming fundamentals.\n"
            "Stage 2: Practice Data Structures and Algorithms.\n"
            "Stage 3: Study OOP, DBMS, OS, and Networks.\n"
            "Stage 4: Build practical software projects.\n"
            "Stage 5: Learn Git and GitHub.\n"
            "Stage 6: Prepare for technical interviews.\n"
            "Stage 7: Apply for internships and software roles.\n\n"
            "Focus on understanding concepts and building consistently."
        )

    # 9. Programming guidance
    elif any(word in question for word in [
        "programming", "coding", "python", "java", "c++", "language"
    ]):
        return (
            "To improve your programming skills:\n\n"
            "1. Choose one primary programming language.\n"
            "2. Understand variables, loops, functions, and arrays.\n"
            "3. Practice basic coding problems.\n"
            "4. Learn Data Structures and Algorithms.\n"
            "5. Build small projects.\n"
            "6. Gradually solve more challenging problems.\n\n"
            "Consistency and problem-solving practice are important."
        )

    # 10. Default response
    return (
        "I'm VoxPath, your voice-powered career mentor!\n\n"
        "I can help you with:\n"
        "1. Career guidance.\n"
        "2. Programming and DSA.\n"
        "3. Project recommendations.\n"
        "4. Internship preparation.\n"
        "5. Resume improvement.\n"
        "6. Technical interview preparation.\n"
        "7. Learning roadmaps.\n\n"
        "Tell me what you want to achieve, and let's plan "
        "your next steps."
    )