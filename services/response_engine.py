def generate_response(user_text, conversation_history=None):

    question = user_text.lower().strip()



    # 1. Context-aware follow-up questions
    if any(phrase in question for phrase in [
        "which one", "which is best", "tell me more",
        "explain more", "that one", "the first one",
        "the second one", "the last one"
    ]):

        if conversation_history:
            previous_response = conversation_history[-1]["assistant"].lower()

            if "student management" in previous_response:
                return (
                    "For a beginner, I recommend starting with a "
                    "student management system. It helps you learn "
                    "Python, databases, CRUD operations, and application "
                    "development. You can gradually add advanced features."
                )

    # 2. Project recommendations
    if any(word in question for word in [
        "project", "projects", "portfolio"
    ]):

        if "python" in question:
            return (
                "Here are five Python project ideas:\n\n"
                "1. Student Management System - Manage student records "
                "using Python and SQLite.\n\n"
                "2. Smart Expense Tracker - Track expenses using "
                "Python and Flask.\n\n"
                "3. AI Career Assistant - Build a career guidance chatbot.\n\n"
                "4. Weather Forecast Application - Display weather "
                "information using Python.\n\n"
                "5. Smart Complaint Management System - Track complaints "
                "using Flask and SQLite.\n\n"
                "For beginners, I recommend starting with the "
                "Student Management System."
            )

        return (
            "Here are some project ideas: an AI-powered personal assistant, "
            "a student management system, a smart expense tracker, or a "
            "career guidance platform."
        )

    # 3. Internship guidance
    elif any(word in question for word in [
    "internship", "intern", "work experience"
]) and not any(word in question for word in [
    "resume", "cv", "github", "linkedin"
]):
        return (
            "To prepare for software internships, focus on programming, "
            "data structures and algorithms, and practical projects. "
            "Build a professional resume, maintain your GitHub profile, "
            "and apply consistently to relevant opportunities."
        )

    # 4. Interview preparation
    elif any(word in question for word in [
        "interview", "mock interview", "technical round"
    ]):
        return (
            "For software interviews, prepare programming fundamentals, "
            "data structures, algorithms, object-oriented programming, "
            "DBMS, operating systems, and computer networks. Also practice "
            "explaining your projects clearly."
        )

    # 5. Resume guidance
    elif any(word in question for word in [
        "resume", "cv", "github", "linkedin"
    ]):
        return (
            "A strong software engineering resume should highlight your "
            "technical skills, projects, achievements, and certifications. "
            "Include project descriptions explaining the problem, "
            "technologies used, and your contribution."
        )

    # 6. Learning roadmap
    elif any(word in question for word in [
        "roadmap", "learning path", "where should i start"
    ]):
        return (
            "A useful software development roadmap starts with programming "
            "fundamentals, followed by data structures and algorithms, "
            "database management, practical projects, Git and GitHub, "
            "and technical interview preparation."
        )

    # 7. Programming guidance
    elif any(word in question for word in [
        "programming", "coding", "python", "java", "c++", "language"
    ]):
        return (
            "To improve your programming skills, start by strengthening "
            "your fundamentals in one programming language. Practice "
            "problem solving regularly, learn data structures and "
            "algorithms, and gradually solve intermediate coding problems."
        )

    # 8. Default response
    else:
        return (
            "Hello! I am VoxPath, your voice-powered career mentor. "
            "I can help you with programming, internships, project ideas, "
            "resume preparation, technical interviews, and learning "
            "roadmaps. Could you tell me more about what you need?"
        )