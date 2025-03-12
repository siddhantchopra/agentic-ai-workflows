# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from crewai import Agent, Task, Crew
# from pydantic import BaseModel
# import time
# import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()
# os.environ["CREWAI_ENABLE_TELEMETRY"] = "false"
# openai_api_key = os.getenv("OPENAI_API_KEY")

# if not openai_api_key:
#     raise ValueError("❌ OPENAI_API_KEY is missing. Check your .env file.")

# os.environ["OPENAI_API_KEY"] = openai_api_key

# # Initialize FastAPI app
# app = FastAPI()

# # Enable CORS for frontend integration
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Set specific frontend domains if needed
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Define Agents
# thinker_agent = Agent(
#     name="Thinker",
#     role="Strategist",
#     goal="Develop a compelling and structured blog outline that aligns with the user’s vision and engages the target audience.",
#     backstory="A seasoned strategist with a knack for transforming raw ideas into captivating narratives. Known for crafting frameworks that resonate with readers and drive engagement.",
#     description="Designs a detailed and engaging blog outline, ensuring the user’s input is the foundation while adding strategic structure for maximum impact."
# )

# researcher_agent = Agent(
#     name="Researcher",
#     role="Data Analyst",
#     goal="Provide accurate, minimal, and relevant research to support the blog without overshadowing the user’s voice.",
#     backstory="A meticulous data analyst with a passion for uncovering facts and insights. Ensures every piece of information enhances the blog’s credibility and depth.",
#     description="Enhances the blog with precise, well-researched details, maintaining a balance between user input and factual accuracy."
# )

# seo_agent = Agent(
#     name="SEO Specialist",
#     role="SEO Expert",
#     goal="Optimize the blog for search engines by integrating targeted keywords, meta descriptions, and SEO-friendly headers.",
#     backstory="A digital marketing expert with a proven track record of boosting online visibility. Specializes in making content discoverable without compromising its quality.",
#     description="Strategically incorporates SEO elements to improve search rankings while keeping the blog natural and reader-friendly."
# )

# writer_agent = Agent(
#     name="Writer",
#     role="Content Creator",
#     goal="Transform the outline and user input into a polished, engaging, and reader-centric blog post.",
#     backstory="A creative wordsmith with a talent for storytelling. Known for crafting content that captivates audiences and communicates ideas effectively.",
#     description="Writes a well-structured, engaging blog post that prioritizes the user’s input while ensuring clarity, flow, and impact."
# )

# image_agent = Agent(
#     name="Image Finder",
#     role="Visual Content Curator",
#     goal="Curate visually appealing and relevant images that complement the blog’s theme and enhance reader engagement.",
#     backstory="A visual content expert with an eye for design and aesthetics. Specializes in selecting images that elevate the blog’s appeal and align with its message.",
#     description="Finds or suggests high-quality images that match the blog’s tone and subject matter, ensuring a visually cohesive experience."
# )

# compiler_agent = Agent(
#     name="Compiler",
#     role="Editor",
#     goal="Assemble and refine all sections into a cohesive, polished, and publication-ready blog post.",
#     backstory="A detail-oriented editor with a passion for perfection. Known for seamlessly blending content, visuals, and formatting into a professional final product.",
#     description="Formats, structures, and finalizes the blog, ensuring it is visually appealing, error-free, and ready for publication."
# )

# # Define Tasks
# def create_tasks(topic, user_details):
#     """Dynamically creates tasks for CrewAI"""
#     return [
#         Task(
#             agent=thinker_agent,
#             description=f"Analyze the topic '{topic}' and user-provided details: {user_details}. Create a structured and engaging blog outline that aligns with the user's vision and resonates with the target audience.",
#             expected_output="A detailed and compelling blog outline, including sections, subheadings, and key points to be covered."
#         ),
#         Task(
#             agent=researcher_agent,
#             description=f"Conduct minimal but precise research to support the user-provided details: {user_details}. Ensure the research enhances the blog's credibility without overshadowing the user's voice.",
#             expected_output="A concise list of factual details, statistics, or references that complement the user's input."
#         ),
#         Task(
#             agent=seo_agent,
#             description=f"Optimize the blog content for search engines by integrating relevant keywords, meta descriptions, and SEO-friendly headers. Ensure the content remains natural and reader-friendly.",
#             expected_output="An SEO-optimized version of the blog outline, including keyword placement, meta tags, and headers."
#         ),
#         Task(
#             agent=writer_agent,
#             description=f"Transform the structured outline and user-provided details: {user_details} into a polished, engaging, and reader-centric blog post. Prioritize clarity, flow, and impact.",
#             expected_output="A fully written, engaging, and well-structured blog draft that aligns with the user's vision."
#         ),
#         Task(
#             agent=image_agent,
#             description=f"Curate or suggest visually appealing images that complement the blog's theme and enhance reader engagement. Ensure the visuals align with the topic '{topic}' and user details: {user_details}.",
#             expected_output="A set of high-quality, relevant images or visual placeholders that match the blog's tone and subject matter."
#         ),
#         Task(
#             agent=compiler_agent,
#             description="Compile and refine all sections of the blog, including the written content, SEO elements, and visuals, into a cohesive and polished final draft. Ensure the blog is error-free and ready for publication.",
#             expected_output="A fully formatted, publication-ready blog post with seamless integration of text, visuals, and SEO elements."
#         )
#     ]

# class BlogRequest(BaseModel):
#     topic: str
#     user_details: str

# # Blog Generation API
# @app.post("/generate-blog")
# async def generate_blog(request: BlogRequest):
#     """
#     Generates a blog using CrewAI and returns the final content.
#     """
#     try:
#         print(f"\n🚀 Generating blog on: {request.topic}\n")
#         print(f"📌 User-provided details: {request.user_details}\n")

#         start_time = time.time()

#         # Create a new Crew with dynamically generated tasks
#         blog_crew = Crew(
#             agents=[thinker_agent, researcher_agent, seo_agent, writer_agent, image_agent, compiler_agent],
#             tasks=create_tasks(request.topic, request.user_details)
#         )

#         results = blog_crew.kickoff()  # Execute workflow
#         final_output = "\n".join(results) if isinstance(results, list) else str(results)

#         # Save blog with timestamp
#         timestamp = time.strftime("%Y%m%d-%H%M%S")
#         file_path = f"generated_blog_{timestamp}.txt"
#         with open(file_path, "w", encoding="utf-8") as file:
#             file.write(final_output)

#         end_time = time.time()
#         print(f"\n✅ Blog generation completed in {round(end_time - start_time, 2)} seconds!")
#         print(f"📂 Blog saved to: {file_path}")

#         return {"message": "Blog generated successfully!", "blog_content": final_output, "file_path": file_path, "execution_time": round(end_time - start_time, 2)}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"❌ Error generating blog: {e}")

# # Run FastAPI server (only when executed directly)
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


# import uvicorn
# from config import app  # Import FastAPI app from config.py
# from routes import router  # Import API routes

# # Include Routes
# app.include_router(router)

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)



from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from crewai import Agent, Task, Crew
import os
import asyncio
from dotenv import load_dotenv


# Load environment variables
load_dotenv()
os.environ["CREWAI_ENABLE_TELEMETRY"] = "false"
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("❌ OPENAI_API_KEY is missing. Check your .env file.")

os.environ["OPENAI_API_KEY"] = openai_api_key

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define CrewAI Agents
thinker_agent = Agent(
    name="Thinker",
    role="Strategist",
    goal="Develop a compelling and structured blog outline that aligns with the user’s vision and engages the target audience.",
    backstory="A seasoned strategist with a knack for transforming raw ideas into captivating narratives. Known for crafting frameworks that resonate with readers and drive engagement.",
    description="Designs a detailed and engaging blog outline, ensuring the user’s input is the foundation while adding strategic structure for maximum impact."
)

researcher_agent = Agent(
    name="Researcher",
    role="Data Analyst",
    goal="Provide accurate, minimal, and relevant research to support the blog without overshadowing the user’s voice.",
    backstory="A meticulous data analyst with a passion for uncovering facts and insights. Ensures every piece of information enhances the blog’s credibility and depth.",
    description="Enhances the blog with precise, well-researched details, maintaining a balance between user input and factual accuracy."
)

seo_agent = Agent(
    name="SEO Specialist",
    role="SEO Expert",
    goal="Optimize the blog for search engines by integrating targeted keywords, meta descriptions, and SEO-friendly headers.",
    backstory="A digital marketing expert with a proven track record of boosting online visibility. Specializes in making content discoverable without compromising its quality.",
    description="Strategically incorporates SEO elements to improve search rankings while keeping the blog natural and reader-friendly."
)

writer_agent = Agent(
    name="Writer",
    role="Content Creator",
    goal="Transform the outline and user input into a polished, engaging, and reader-centric blog post.",
    backstory="A creative wordsmith with a talent for storytelling. Known for crafting content that captivates audiences and communicates ideas effectively.",
    description="Writes a well-structured, engaging blog post that prioritizes the user’s input while ensuring clarity, flow, and impact."
)

image_agent = Agent(
    name="Image Finder",
    role="Visual Content Curator",
    goal="Curate visually appealing and relevant images that complement the blog’s theme and enhance reader engagement.",
    backstory="A visual content expert with an eye for design and aesthetics. Specializes in selecting images that elevate the blog’s appeal and align with its message.",
    description="Finds or suggests high-quality images that match the blog’s tone and subject matter, ensuring a visually cohesive experience."
)

compiler_agent = Agent(
    name="Compiler",
    role="Editor",
    goal="Assemble and refine all sections into a cohesive, polished, and publication-ready blog post.",
    backstory="A detail-oriented editor with a passion for perfection. Known for seamlessly blending content, visuals, and formatting into a professional final product.",
    description="Formats, structures, and finalizes the blog, ensuring it is visually appealing, error-free, and ready for publication."
)

# Define Task Creation
def create_tasks(topic, user_details):
    return [
        Task(
            agent=thinker_agent,
            description=f"Analyze the topic '{topic}' and user-provided details: {user_details}. Create a structured and engaging blog outline that aligns with the user's vision and resonates with the target audience.",
            expected_output="A detailed and compelling blog outline, including sections, subheadings, and key points to be covered."
        ),
        Task(
            agent=researcher_agent,
            description=f"Conduct minimal but precise research to support the user-provided details: {user_details}. Ensure the research enhances the blog's credibility without overshadowing the user's voice.",
            expected_output="A concise list of factual details, statistics, or references that complement the user's input."
        ),
        Task(
            agent=seo_agent,
            description=(
                f"Optimize the blog content for search engines based on the topic '{topic}' and user preferences: {user_details}. "
                "Integrate relevant keywords, meta descriptions, and SEO-friendly headers. Ensure the content remains natural and reader-friendly."
            ),
            expected_output="An SEO-optimized version of the blog outline, including keyword placement, meta tags, and headers."
        ),
        Task(
            agent=writer_agent,
            description=f"Transform the structured outline and user-provided details: {user_details} into a polished, engaging, and reader-centric blog post. Prioritize clarity, flow, and impact.",
            expected_output="A fully written, engaging, and well-structured blog draft that aligns with the user's vision."
        ),
        Task(
            agent=image_agent,
            description=f"Curate or suggest visually appealing images that complement the blog's theme and enhance reader engagement. Ensure the visuals align with the topic '{topic}' and user details: {user_details}.",
            expected_output="A set of high-quality, relevant images or visual placeholders that match the blog's tone and subject matter."
        ),
        Task(
            agent=compiler_agent,
            description="Compile and refine all sections of the blog, including the written content, SEO elements, and visuals, into a cohesive and polished final draft. Ensure the blog is error-free and ready for publication.",
            expected_output="A fully formatted, publication-ready blog post with seamless integration of text, visuals, and SEO elements."
        )
    ]

# Streaming Generator Function
async def task_progress_generator(topic: str, user_details: str):
    """Streams real-time task execution results via SSE"""

    tasks = create_tasks(topic, user_details)
    agents = [thinker_agent, researcher_agent, seo_agent, writer_agent, image_agent, compiler_agent]
    crew = Crew(agents=agents, tasks=tasks)

    # ✅ STREAM INDIVIDUAL TASKS
    for task in tasks:
        assigned_agent = task.agent  
        result = await asyncio.to_thread(assigned_agent.execute_task, task) 

        update = f"{assigned_agent.role} completed: {result} ✅"
        update = update.replace("\n", "<br>")  # ✅ Keep formatting clean
        yield f"data: {update}\n\n"
        await asyncio.sleep(0.1)

    yield f"data: 🚀 Running final crew workflow...<br>\n\n"
    await asyncio.sleep(0.1)

    # ✅ RUN FINAL WORKFLOW & ENSURE FULL OUTPUT
    final_results = await asyncio.to_thread(crew.kickoff)

    if not final_results:
        final_output = "⚠️ No content generated!"
    elif isinstance(final_results, list):
        final_output = "\n\n".join(map(str, final_results))
    else:
        final_output = str(final_results)

    # ✅ PRESERVE NEWLINES SAFELY
    final_output = final_output.replace("\n", "<b>")  

    # ✅ SPLIT OUTPUT TO ENSURE NOTHING BREAKS
    chunk_size = 500  
    for i in range(0, len(final_output), chunk_size):
        chunk = final_output[i:i+chunk_size]
        yield f"data: {chunk}\n\n"
        await asyncio.sleep(0.1)

    yield "data: ✅ Blog Generation Complete!<br>\n\n"

@app.get("/stream")
async def stream_sse(topic: str, user_details: str):
    """SSE endpoint for real-time task updates"""
    return StreamingResponse(task_progress_generator(topic, user_details), media_type="text/event-stream")