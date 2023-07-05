import discord
import asyncio
from webserver import keep_alive
import json
import random
import os

# Defining client
itemdesc={'water':'A bottle of water which increases your earnings of a job when','old fishing rod':'A fishing rod that allows you to catch normal fish','potato':'Just a potato?','silver rod':'A fishing rod that allows you to catch silver fish', 'golden rod':'A fishing rod that allows you to catch golden fish','platinum rod':'A fishing rod that allows you to catch platinum fish', 'fish food': 'Increases the chances of catching a fish'}
price={'water':1000,'old fishing rod':2000,'potato':3000}
items=['water','old fishing rod','potato']
fitems=['silver rod', 'golden rod','platinum rod', 'fish food']
fishprice={'silver rod': 100, 'golden rod':500,'platinum rod': 1000, 'fish food':50}
fisher=['koi','flowerhorn','arowana','axolotl','pufferfish','swordfish','tilapia','cod','salmon','goldfish','sardine','tuna']
fishesprice={'koi': 1000,'flowerhorn':900,'arowana':800,'axolotl':650,'pufferfish':600,'swordfish':550,'tilapia':450,'cod':400,'salmon':300,'tuna':200,'sardine':100,'goldfish':50}
platfish=['koi','flowerhorn','arowana']
goldfish=['axolotl','pufferfish','swordfish']
silverfish=['tilapia','cod','salmon']
normalfish=['goldfish','sardine','tuna']
  #opening Json to define client
with open('fishfood.json') as file_object:
  fishfood=json.load(file_object)
with open('fbal.json') as file_object:
  fbal=json.load(file_object)
with open('bal.json') as file_object:
  bal=json.load(file_object)
with open('inv.json') as file_object:
  inv=json.load(file_object)
with open('fish.json') as file_object:
  fishes=json.load(file_object)
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)
numbers = [10, 20, 30, 70, 191, 23]  
filename = 'numbers.json'        
with open(filename, 'w') as file_object:  
 json.dump(numbers, file_object)  
# Command syncing
@client.event
async def on_ready():
    await asyncio.sleep(2)
    await tree.sync()
    print("Ready!")
# Creating commands
@tree.command(name='helloworld', description='Says Hello World')
async def helloword(interaction: discord.Interaction):
    await interaction.response.send_message("Hello World!")
@tree.command(name='create', description='creates your profile')
async def profile(interaction: discord.Interaction ):
  if str(interaction.user.id) in bal:
    await interaction.response.send_message('You have already created a profile!')
  else:  
    await interaction.response.send_message("We have created your profile, {}.".format(interaction.user.display_name))
    bal[str(interaction.user.id)]=0
    fbal[str(interaction.user.id)]=0
    fishfood[str(interaction.user.id)]=0
    inv[str(interaction.user.id)]={}
    fishes[str(interaction.user.id)]={}
  with open('bal.json', 'w') as file_object:  
      json.dump(bal, file_object) 
  with open('inv.json', 'w') as file_object:  
      json.dump(inv, file_object)
  with open('fbal.json', 'w') as file_object:  
      json.dump(fbal, file_object)
  with open('fishfood.json', 'w') as file_object:  
      json.dump(fishfood, file_object)
  with open('fish.json', 'w') as file_object:  
      json.dump(fishes, file_object)
@tree.command(name='numbers', description='just random numbers')
async def numbers(interaction: discord.Interaction ):
    with open('numbers.json') as file_object:  
      data=json.load(file_object)
    await interaction.response.send_message(data)

@tree.command(name='work', description='work for money')
@discord.app_commands.checks.cooldown(1, 10.0, key=lambda i: i.user.id)
async def work(interaction: discord.Interaction):
    if str(interaction.user.id) in bal:  
      f=random.randint(200,600)
      per=1
      fs=''
      st=''
      t=random.randint(1,100)
      if f < 300:
        l='mcdonalds'
      elif f<400:
        l='a factory'
      elif f<500:
        l='a customer service centre'
      else:
        l='a hospital'
      for i in inv[str(interaction.user.id)]:
        if i=='water':
          per+=0.001*inv[str(interaction.user.id)][i]
          fs+= 'water, '
        elif i=='potato':
          per+=0.01*inv[str(interaction.user.id)][i]
          fs+= 'potato, '
      if per>1 and t<=20:
        f=int(f*per)
        per=round((per-1)*100,2)
        fs=fs[:-2]+' at an additional {}%'.format(per)
        st=' You have earned a bonus due to {}.'.format(fs)
      await interaction.response.send_message("You have earned ${} for working at {}.{}".format(f,l,st))
      bal[str(interaction.user.id)]+= f
    else:
      await interaction.response.send_message("Please create your profile with /create")
    with open('bal.json', 'w') as file_object:  
      json.dump(bal, file_object) 
@work.error
async def on_test_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    if isinstance(error, discord.app_commands.CommandOnCooldown):
        await interaction.response.send_message(str(error), ephemeral=True)
@tree.command(name='balance', description='The amount of money you have')
async def balance(interaction: discord.Interaction ):
  if str(interaction.user.id) in bal:
    bal_embed = discord.Embed(title="{}'s balance".format(interaction.user.display_name))
    balances='• $ {} Cash\n• 🟡 {} Fishing token'.format(str(bal[str(interaction.user.id)]),str(fbal[str(interaction.user.id)]))
    bal_embed.add_field(name='You currently have:', value=balances)
    await interaction.response.send_message(embed=bal_embed)
  else:
    await interaction.response.send_message("Please create your profile with /create!")
@tree.command(name='shop_view', description='A place where you can buy stuff')
async def shopview(interaction: discord.Interaction):
  if str(interaction.user.id) in bal:  
    shop_embed = discord.Embed(title="Shop")
    shop_embed.add_field(name=' ', value="water: $1000\nOld Fishing rod: $2000\npotato: $3000")
    await interaction.response.send_message(embed=shop_embed)
  else:
    await interaction.response.send_message("Please create your profile with /create!")
@tree.command(name='shop_buy', description='A place to buy items from the store!')
async def shopbuy(interaction: discord.Interaction, item: str):
  item =item.lower()
  if str(interaction.user.id) in bal:  
    if item in items:
      if bal[str(interaction.user.id)]>price[item]:
        if item in inv[str(interaction.user.id)]:
          inv[str(interaction.user.id)][item]+=1
        else:
          inv[str(interaction.user.id)][item]=1
        bal[str(interaction.user.id)]-= price[item]
        await interaction.response.send_message('You have purchased {}'.format(item)) 
      else:
        await interaction.response.send_message('You do not have enough money for {}.'.format(item))
    else:
      await interaction.response.send_message('Invalid item')
    with open('bal.json', 'w') as file_object:  
      json.dump(bal, file_object) 
    with open('inv.json', 'w') as file_object:  
      json.dump(inv, file_object) 
  else:
    await interaction.response.send_message("Please create your profile with /create!")
@tree.command(name='inventory', description='Your inventory where you keep your items!')
async def inve(interaction: discord.Interaction):
  if str(interaction.user.id) in bal:  
    invent=''
    for i in inv[str(interaction.user.id)]:
      invent+=str(inv[str(interaction.user.id)][i])+'x '+i+'\n'
    inv_embed = discord.Embed(title="Inventory")
    inv_embed.add_field(name=' ', value=invent)
    await interaction.response.send_message(embed=inv_embed)
  else:
    await interaction.response.send_message("Please create your profile with /create!")
@tree.command(name='leaderboard', description='A leaderboard to show the amount of money everyone has')
async def leaderboard(interaction: discord.Interaction):
  global bal
  if str(interaction.user.id) in bal:  
    lb=''
    count=1
    bal = dict(reversed(sorted(bal.items(), key=lambda x:x[1])))
    for key,value in bal.items():
      lb+=str(count)+'. ' + client.get_user(int(key)).name+': $'+str(value)+'\n'
      count+=1
    inv_embed = discord.Embed(title="Leaderboard")
    inv_embed.add_field(name=' ', value=lb)
    await interaction.response.send_message(embed=inv_embed)
    with open('bal.json','w') as file_object:
      json.dump(bal,file_object,)
  else:
    await interaction.response.send_message("Please create your profile with /create!")

@tree.command(name='help',description='help')
async def help(interaction:discord.Interaction):
  embed = discord.Embed(title='Help command')
  for command in tree.walk_commands():
    embed.add_field(name=command.name, value=command.description)
  await interaction.response.send_message(embed=embed)
@tree.command(name='fish',description='You can catch fish with your fishing rod!')
async def fish(interaction:discord.Interaction):
  if str(interaction.user.id) in bal:
    if 'old fishing rod' in inv[str(interaction.user.id)]:
      view = discord.ui.View()
      f=0
      mybutton = discord.ui.Button(label='cast')
      async def mybutton_callback(interaction: discord.Interaction):
        f=random.randint(1,2)
        if fishfood[str(interaction.user.id)]>0:
          fishfood[str(interaction.user.id)]-=1
          f=random.randint(1,4)
          if f>=2:
            f=2
          else:
            f=1
        else:
          f=random.randint(1,2)
        if f==2:
          mybutton.label='✅'
          mybutton.disabled=True
          if 'platinum rod' in inv[str(interaction.user.id)]:
            fi=platfish[random.randint(0,2)]
            fbal[str(interaction.user.id)]+=10
          elif 'golden rod' in inv[str(interaction.user.id)]:
            fi= goldfish[random.randint(0,2)]
            fbal[str(interaction.user.id)]+=5
          elif 'silver rod' in inv[str(interaction.user.id)]:
            fi= silverfish[random.randint(0,2)]
            fbal[str(interaction.user.id)]+=3
          else:
            fi=normalfish[random.randint(0,2)]
            fbal[str(interaction.user.id)]+=1
          if fi in fishes[str(interaction.user.id)]:
            fishes[str(interaction.user.id)][fi]+=1
          else:
            fishes[str(interaction.user.id)][fi]=1
          await interaction.response.edit_message(content='You have caught a {} fish!'.format(fi),view=view)
          with open('fbal.json', 'w') as file_object:  
            json.dump(fbal, file_object) 
          with open('fish.json','w') as file_object:
             json.dump(fishes,file_object)
        else:
          mybutton.label='❌'
          mybutton.disabled=True
          await interaction.response.edit_message(content='Your fish has drowned!',view=view)
    # Callback function
      #view.timeout=10
      mybutton.callback = mybutton_callback
      view.add_item(mybutton)
      await interaction.response.send_message('Fishing...', view=view)
      await asyncio.sleep(10)
      if asyncio.sleep==0:
        if f==0:
          mybutton.label='❌'
          mybutton.disabled=True
          await interaction.edit_original_response(content='Your fish has flown away!',view=view)
    else:
      await interaction.response.send_message("You do not have a fishing rod! You can get it from the shop!")
  else:
    await interaction.response.send_message("Please create your profile with /create!")
@tree.command(name='fish_shop',description='A shop where you can view what to buy with your fishing tokens!')
async def fishshop(interaction:discord.Interaction):
  if str(interaction.user.id) in bal:  
    fshop_embed = discord.Embed(title="Shop")
    fshop_embed.add_field(name=' ', value='Silver rod: 100{0}\nGolden rod:500{0}\nPlatinum rod: 1000{0}\n Fish food:50{0}'.format('🟡'))
    await interaction.response.send_message(embed=fshop_embed)
  else:
    await interaction.response.send_message("Please create your profile with /create!")
@tree.command(name='fish_buy',description='A shop where you can view what to buy with your fishing tokens!')
async def fish_buy(interaction:discord.Interaction,item:str):
  item =item.lower()
  if str(interaction.user.id) in bal:  
    if item in fitems:
      if fbal[str(interaction.user.id)]>fishprice[item]:
        if item in inv[str(interaction.user.id)]:
            inv[str(interaction.user.id)][item]+=1
        else:
          inv[str(interaction.user.id)][item]=1
        fbal[str(interaction.user.id)]-= fishprice[item]
        await interaction.response.send_message('You have purchased {}'.format(item)) 
      else:
        await interaction.response.send_message('You do not have enough 🟡 for {}.'.format(item))
    else:
      await interaction.response.send_message('Invalid item')
    with open('fbal.json', 'w') as file_object:
      json.dump(fbal, file_object) 
    with open('inv.json', 'w') as file_object:  
      json.dump(inv, file_object)  
  else:
    await interaction.response.send_message("Please create your profile with /create!")
@tree.command(name='fishsell', description='sell your fish for money')
async def fishsell(interaction: discord.Interaction,fish:str,quantity:int):
  if str(interaction.user.id) in bal:  
    if fish in fisher:
      if fish in fishes[str(interaction.user.id)]:
        if quantity<=fishes[str(interaction.user.id)][fish]:
          s= fishesprice[fish]*quantity
          bal[str(interaction.user.id)]+=s
          fishes[str(interaction.user.id)][fish]-=quantity
          if fishes[str(interaction.user.id)][fish]==0:
           del fishes[str(interaction.user.id)][fish]
          await interaction.response.send_message('You have sold {} {} for ${}'.format(quantity,fish,s))
          with open('bal.json', 'w') as file_object:  
            json.dump(bal, file_object) 
          with open('fish.json', 'w') as file_object:  
            json.dump(fishes, file_object)
        else:
          await interaction.response.send_message('You do not have enough {} to sell'.format(fish))
      else:
        await interaction.response.send_message('You do not have this fish. Do /fish in order to get some fishes!')
    else:
      await interaction.response.send_message('Invalid fish! please enter a valid fish!')
  else:
    await interaction.response.send_message("Please create your profile with /create!")
@tree.command(name='fish_inventory',description='The fishes that you have!')
async def fishinv(interaction:discord.Interaction):
  if str(interaction.user.id) in bal:  
    fis=''
    for i in fishes[str(interaction.user.id)]:
      fis+=str(fishes[str(interaction.user.id)][i])+'x '+i+'\n'
    inv_embed = discord.Embed(title="Fish Inventory")
    inv_embed.add_field(name=' ', value=fis)
    await interaction.response.send_message(embed=inv_embed)
  else:
    await interaction.response.send_message("Please create your profile with /create!")
@tree.command(name='fishfood',description='Use your fishfood!')
async def ffoo(interaction:discord.Interaction,quantity:int):
  if str(interaction.user.id) in bal:  
    if 'fish food' in inv[str(interaction.user.id)]:
      if inv[str(interaction.user.id)]['fish food']>0:
        if inv[str(interaction.user.id)]['fish food']>=quantity:
          fuses=10*quantity
          if str(interaction.user.id) in fishfood:
            fishfood[str(interaction.user.id)]+=fuses
          else:
            fishfood[str(interaction.user.id)]=fuses
          await interaction.response.send_message("You have used {} fishfood for {} catches!".format(quantity,fuses))
        else:
          await interaction.response.send_message("You do not have enough fish food. Please buy some from the fish shop to use it")
      else:
          await interaction.response.send_message("You do not have any fish food. Please buy some from the fish shop to use it")
    else:
      await interaction.response.send_message("You do not have any fish food. Please buy some from the fish shop to use it")
    with open('inv.json', 'w') as file_object:  
      json.dump(inv, file_object)  
    with open('fishfood.json', 'w') as file_object:  
      json.dump(fishfood, file_object) 
  else:
    await interaction.response.send_message("Please create your profile with /create!")
@tree.command(name='fish_catalogue',description='The fishes that you have!')
async def fishcatalogue(interaction:discord.Interaction):
  if str(interaction.user.id) in bal:  
    embed = discord.Embed(title='Fish Catalogue')
    for i , p in sorted(fishesprice.items(), key=lambda x: x[1]):
      embed.add_field(name=i, value='$'+str(p))
    await interaction.response.send_message(embed=embed)
  else:
    await interaction.response.send_message("Please create your profile with /create!")
@tree.command(name='invest',description='gimme ur money!')
async def invest(interaction:discord.Interaction):
  if str(interaction.user.id) in bal:  
    await interaction.response.send_message("You have been scammed!")
  else:
    await interaction.response.send_message("Please create your profile with /create!")
@tree.command(name='item_description',description='View information about your items')
async def itemdescr(interaction:discord.Interaction,item:str):
  if str(interaction.user.id) in bal:
    if item.lower() in itemdesc:
      item_embed = discord.Embed(title="Item description")
      if item in inv[str(interaction.user.id)]:
        noitem=inv[str(interaction.user.id)][item]
      else:
        noitem='none'
      it=itemdesc[item]+'\n\nYou own {}!'.format(noitem)
      item_embed.add_field(name=item.lower(), value=it)
      await interaction.response.send_message(embed=item_embed)
    else:
      await interaction.response.send_message('This item does not exist!')
  else:
    await interaction.response.send_message("Please create your profile with /create!")
keep_alive()
client.run(os.environ['token'])