from fastapi import APIRouter, HTTPException
from models import BlogRequest
from tasks import create_tasks
from agents import agents
from crewai import Crew
import time

router = APIRouter()

@router.post("/generate-blog")
async def generate_blog(request: BlogRequest):
    """
    Generates a blog using CrewAI and returns the final content.
    """
    try:
        print(f"\n🚀 Generating blog on: {request.topic}\n📌 User details: {request.user_details}")

        start_time = time.time()

        blog_crew = Crew(agents=agents, tasks=create_tasks(request.topic, request.user_details))
        results = blog_crew.kickoff()
        final_output = "\n".join(results) if isinstance(results, list) else str(results)

        # Save to file
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        file_path = f"generated_blog_{timestamp}.txt"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(final_output)

        execution_time = round(time.time() - start_time, 2)
        print(f"\n✅ Blog generation completed in {execution_time} seconds!")

        return {"message": "Blog generated successfully!", "blog_content": final_output, "file_path": file_path, "execution_time": execution_time}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Error generating blog: {e}")
