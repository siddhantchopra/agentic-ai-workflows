from crewai import Task
from agents import thinker_agent, researcher_agent, seo_agent, writer_agent, image_agent, compiler_agent

def create_tasks(topic, user_details):
    """Dynamically creates tasks for CrewAI"""
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
            description=f"Optimize the blog content for search engines by integrating relevant keywords, meta descriptions, and SEO-friendly headers. Ensure the content remains natural and reader-friendly.",
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
