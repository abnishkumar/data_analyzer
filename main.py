import logging
from data_analysis_runner import DataAnalysisRunner


async def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    try:
        async with DataAnalysisRunner() as runner:
            task = "Analyze iris.csv dataset"
            
            async for message in runner.analyze_data(task):
                print(message.content)
                
    except Exception as e:
        logging.error("Analysis failed: %s", e)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())