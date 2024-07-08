import aiohttp, random
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

async def recipe_parse():
    headers = {'user-agent': UserAgent().random}
    recipe = random.randint(1, 300000)
    # recipe = 200000 # error 404'
    # recipe = 786615 # "чистый рецепт"
    # recipe = 215630 # БЖУ разделить
    # recipe = 118162 # с отдельной последней строкой
    main_url = 'https://chef.tm'
    recipe_url = 'https://chef.tm/recipe/'
    async with aiohttp.ClientSession() as session:
        session: aiohttp.ClientSession 
        response = await session.get(f'{recipe_url}{recipe}', headers=headers)
        # print(f'{recipe_url}{recipe}')
        if response.ok:
            soup = BeautifulSoup(await response.text(), 'lxml')
            try:
                title = soup.find('h2', class_='zblock-title').text.strip()
                recipe_block = soup.find('div', class_='zblock-p') # блок с картинкой и текстом
                recipe_text = f'<b>{title}</b>\n' + recipe_block.find('div', class_='post__text').text.strip()
                recipe_image = main_url + recipe_block.find('div', class_='post__first_image').find('img')['src']
                return recipe_text, recipe_image
            except AttributeError:
                return None
        else:
            await recipe_parse()
        

# collect and format data
async def gather_recipe():
    recipe = await recipe_parse()
    if recipe:
        post_text, image_url = recipe
        if '????' in post_text:
            post_text = post_text.replace('????', ' ~~ ')   
        # print(post_text.split('\n'), len([i for i in post_text.split('\n')]), sep='\n') 
        return post_text, image_url
    return None


if __name__ == '__main__':
    import asyncio
    asyncio.run(gather_recipe())