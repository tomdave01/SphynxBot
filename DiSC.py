import discord
import firebase_admin
from firebase_admin import credentials
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
from trueskill import Rating, quality, rate
from firebase import Firebase 
import random
from firebase_admin import db

Client = discord.Client()
client = commands.Bot(command_prefix = '~')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    print("Bot is online and connected to discord")
    

cred = credentials.Certificate('C:/Users/tomda/Downloads/rpft-bot-firebase-adminsdk-qyeg7-820469b533.json')

config = {
    "apiKey": "", #removed for security
    "authDomain": "rpft-bot.firebaseapp.com",
    "databaseURL": "https://rpft-bot.firebaseio.com",
    "storageBucket": "rpft-bot.appspot.com",
}

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://rpft-bot.firebaseio.com'
})

firebase = Firebase(config)
db = firebase.database()

# As an admin, the app has access to read and write all data, regradless of Security Rules
#ref = firebase_admin.db.reference('https://rpft-bot.firebaseio.com')
#print(ref.get())


def Get_rating(xp1content):
    users = db.child("players").child(xp1content).get()
    xmu = db.child("players").child(xp1content).child('mu').get()
    xsigma = db.child("players").child(xp1content).child('sigma').get()
    x = users.val()
    sigma = xsigma.val()
    mu = xmu.val()

    d,y = float(mu),float(sigma)
    r1 = Rating(d,y)
    return r1

@client.event
async def on_message(message):

        if message.content.upper().startswith('~input_match'):
            major = db.child("major_role").get()
            if major in [role.id for role in message.author.roles]:
                await client.send_message(message.channel, 'How many players on the winning team?')
                win_num_play = await client.wait_for_message(author=message.author)
                await client.send_message(message.channel, 'How many players on the losing team?')
                lose_num_play = await client.wait_for_message(author=message.author)
                await client.send_message(message.channel, 'How many substitutions did the winning team make?')
                win_num_subs = await client.wait_for_message(author=message.author)
                await client.send_message(message.channel, 'How many substitutions did the losing team make?')
                lose_num_subs = await client.wait_for_message(author=message.author)

                team1 = []
                team2 = []
                n = 1
                for i in range (win_num_play.content):
                    await client.send_message(message.channel, 'Name of player' + n + ' on winning team?')
                    player = await client.wait_for_message(author=message.author)
                    team1.append(player.content)
                    n += 1
                return team1

                for i in range (lose_num_play.content):
                    await client.send_message(message.channel, 'Name of player' + n + ' on losing team?')
                    player = await client.wait_for_message(author=message.author)
                    team2.append(player.content)
                    n += 1
                return team2

                

                
            else:
                print ("You don't have the permissions to complete this command :facepalm:")

        '''if message.content.startswith('2v2.db'):
            await client.send_message(message.channel,'Enter player')
            
            xp1 = await client.wait_for_message(author=message.author)
            xp2 = await client.wait_for_message(author=message.author)
            xp3 = await client.wait_for_message(author=message.author)
            xp4 = await client.wait_for_message(author=message.author)
            r1 = Get_rating(xp1.content)
            r2 = Get_rating(xp2.content)
            r3 = Get_rating(xp3.content)
            r4 = Get_rating(xp4.content)

            t1 = [r1,r2]
            t2 = [r3,r4]
            await client.send_message(message.channel,'{:.1%} chance to draw'.format(quality([t1, t2])))
            (new_r1,new_r2,), (new_r3,new_r4) = rate([t1, t2], ranks=[0, 1])

            await client.send_message(message.channel,'Updated rank for P1: '+str(new_r1))
            await client.send_message(message.channel,'Updated rank for P2: '+str(new_r2))
            await client.send_message(message.channel,'Updated rank for P3: '+str(new_r3))
            await client.send_message(message.channel,'Updated rank for P4: '+str(new_r4))
            r1s = new_r1.sigma
            r2s = new_r2.sigma
            r3s = new_r3.sigma
            r4s = new_r4.sigma
            r1m = new_r1.mu
            r2m = new_r2.mu
            r3m = new_r3.mu
            r4m = new_r4.mu
            xrs = [r1s,r2s,r2s,r4s]
            xrm = [r1m,r2m,r3m,r4m]
            print(xrs)
            print(xrm)

            db.child("players").child(xp1.content).update({"mu": r1m})
            db.child("players").child(xp1.content).update({"sigma":r1s})
            db.child("players").child(xp2.content).update({"mu": r2m})
            db.child("players").child(xp2.content).update({"sigma":r2s})
            db.child("players").child(xp3.content).update({"mu": r3m})
            db.child("players").child(xp3.content).update({"sigma":r3s})
            db.child("players").child(xp4.content).update({"mu": r4m})
            db.child("players").child(xp4.content).update({"sigma":r4s})'''

        elif message.content.startswith('check.p'):
            await client.send_message(message.channel, '`how many?`')
            amount_of_players = await client.wait_for_message(author=message.author)
            for i in range(int(amount_of_players.content)):
                xp1 = await client.wait_for_message(author=message.author)
                r1 =Get_rating(xp1.content)
                await client.send_message(message.channel,r1)
            
            
        elif message.content.startswith('set.p'):
            await client.send_message(message.channel, '`Name, mu,sigma`')
            xp3 = await client.wait_for_message(author=message.author)
            xp1 = await client.wait_for_message(author=message.author)
            xp2 = await client.wait_for_message(author=message.author)
            await client.send_message(message.channel, '`pushing data`')
            db.child("players").child(xp3.content).child("mu").set(xp1.content)
            db.child("players").child(xp3.content).child("sigma").set(xp2.content)

        #add player to competition    
        elif message.content.startswith('add_player'):
            await client.send_message(message.channel, '`Name of player?`')
            xp3 = await client.wait_for_message(author=message.author)
            await client.send_message(message.channel, '`Name of team?`')
            xp4 = await client.wait_for_message(author=message.author)
            await client.send_message(message.channel, '`pushing data`')
            db.child("players").child(xp3.content).child("mu").set(25.0)
            db.child("players").child(xp3.content).child("sigma").set(8.333)
            db.child("players").child(xp3.content).child("team").set(xp4.content)
            db.child("players").child(xp3.content).child("Kills").set(0)
            db.child("players").child(xp3.content).child("Deaths").set(0)
            db.child("players").child(xp3.content).child("win%").set(0)
            db.child("players").child(xp3.content).child("rP").set(0)
            db.child("players").child(xp3.content).child("rW").set(0)

        #new team
        '''elif message.content.startswith('add_team'):
            await client.send_message(message.channel, '`Name of team?`')
            xp3 = await client.wait_for_message(author=message.author)
            await client.send_message(message.channel, '`pushing data`')
            db.child("teams").child(xp3.content).child("mu").set(10)
            db.child("teams").child(xp3.content).child("sigma").set(8)'''
            
        #update player stats           
        if message.content.startswith('update_player'):
            await client.send_message(message.channel, '`player name, mu, sigma`')
            xp0 = await client.wait_for_message(author=message.author)
            xp1 = await client.wait_for_message(author=message.author)
            xp2 = await client.wait_for_message(author=message.author)
            await client.send_message(message.channel, '`pushing data`')
            db.child("players").child(xp0.content).update({"mu": xp1.content})
            db.child("players").child(xp0.content).update({"sigma": xp2.content})

        #calculate 4v4s
        elif message.content.startswith('4v4.db'):
            await client.send_message(message.channel,'Enter players:')
            
            xp1 = await client.wait_for_message(author=message.author)
            xp2 = await client.wait_for_message(author=message.author)
            xp3 = await client.wait_for_message(author=message.author)
            xp4 = await client.wait_for_message(author=message.author)
            xp5 = await client.wait_for_message(author=message.author)
            xp6 = await client.wait_for_message(author=message.author)
            xp7 = await client.wait_for_message(author=message.author)
            xp8 = await client.wait_for_message(author=message.author)
            
            r1 =Get_rating(xp1.content)
            r2 =Get_rating(xp2.content)
            r3 =Get_rating(xp3.content)
            r4 =Get_rating(xp4.content)
            r5 =Get_rating(xp5.content)
            r6 =Get_rating(xp6.content)
            r7 =Get_rating(xp7.content)
            r8 =Get_rating(xp8.content)
            
            t1 = [r1,r2,r3,r4]
            t2 = [r5,r6,r7,r8]
            await client.send_message(message.channel,'{:.1%} chance to draw'.format(quality([t1, t2])))
            (new_r1,new_r2,new_r3,new_r4), (new_r5,new_r6,new_r7,new_r8) = rate([t1, t2], ranks=[0, 1])

            await client.send_message(message.channel,'Updated rank for P1: '+str(new_r1))
            await client.send_message(message.channel,'Updated rank for P2: '+str(new_r2))
            await client.send_message(message.channel,'Updated rank for P3: '+str(new_r3))
            await client.send_message(message.channel,'Updated rank for P4: '+str(new_r4))
            await client.send_message(message.channel,'Updated rank for P5: '+str(new_r5))
            await client.send_message(message.channel,'Updated rank for P6: '+str(new_r6))
            await client.send_message(message.channel,'Updated rank for P7: '+str(new_r7))
            await client.send_message(message.channel,'Updated rank for P8: '+str(new_r8))

            
            r1s = new_r1.sigma
            r2s = new_r2.sigma
            r3s = new_r3.sigma
            r4s = new_r4.sigma
            r5s = new_r5.sigma
            r6s = new_r6.sigma
            r7s = new_r7.sigma
            r8s = new_r8.sigma
            r1m = new_r1.mu
            r2m = new_r2.mu
            r3m = new_r3.mu
            r4m = new_r4.mu
            r5m = new_r5.mu
            r6m = new_r6.mu
            r7m = new_r7.mu
            r8m = new_r8.mu
         

            db.child("players").child(xp1.content).update({"mu": r1m})
            db.child("players").child(xp1.content).update({"sigma":r1s})
            db.child("players").child(xp2.content).update({"mu": r2m})
            db.child("players").child(xp2.content).update({"sigma":r2s})
            db.child("players").child(xp3.content).update({"mu": r3m})
            db.child("players").child(xp3.content).update({"sigma":r3s})
            db.child("players").child(xp4.content).update({"mu": r4m})
            db.child("players").child(xp4.content).update({"sigma":r4s})
            
            db.child("players").child(xp5.content).update({"mu": r5m})
            db.child("players").child(xp5.content).update({"sigma":r5s})
            db.child("players").child(xp6.content).update({"mu": r6m})
            db.child("players").child(xp6.content).update({"sigma":r6s})
            db.child("players").child(xp7.content).update({"mu": r7m})
            db.child("players").child(xp7.content).update({"sigma":r7s})
            db.child("players").child(xp8.content).update({"mu": r8m})
            db.child("players").child(xp8.content).update({"sigma":r8s})

        #calculate 5v5s   
        elif message.content.startswith('5v5.db'):
            await client.send_message(message.channel,'Enter players:')
            
            xp1 = await client.wait_for_message(author=message.author)
            xp2 = await client.wait_for_message(author=message.author)
            xp3 = await client.wait_for_message(author=message.author)
            xp4 = await client.wait_for_message(author=message.author)
            xp5 = await client.wait_for_message(author=message.author)
            xp6 = await client.wait_for_message(author=message.author)
            xp7 = await client.wait_for_message(author=message.author)
            xp8 = await client.wait_for_message(author=message.author)
            xp9 = await client.wait_for_message(author=message.author)
            xp10 = await client.wait_for_message(author=message.author)
            
            r1 =Get_rating(xp1.content)
            r2 =Get_rating(xp2.content)
            r3 =Get_rating(xp3.content)
            r4 =Get_rating(xp4.content)
            r5 =Get_rating(xp5.content)
            r6 =Get_rating(xp6.content)
            r7 =Get_rating(xp7.content)
            r8 =Get_rating(xp8.content)
            r9 =Get_rating(xp9.content)
            r10 =Get_rating(xp10.content)
            
            t1 = [r1,r2,r3,r4,r5]
            t2 = [r6,r7,r8,r9,r10]
            await client.send_message(message.channel,'{:.1%} chance to draw'.format(quality([t1, t2])))
            (new_r1,new_r2,new_r3,new_r4, new_r5), (new_r6,new_r7,new_r8,new_r9,new_r10) = rate([t1, t2], ranks=[0, 1])

            await client.send_message(message.channel,'Updated rank for P1: '+str(new_r1))
            await client.send_message(message.channel,'Updated rank for P2: '+str(new_r2))
            await client.send_message(message.channel,'Updated rank for P3: '+str(new_r3))
            await client.send_message(message.channel,'Updated rank for P4: '+str(new_r4))
            await client.send_message(message.channel,'Updated rank for P5: '+str(new_r5))
            await client.send_message(message.channel,'Updated rank for P6: '+str(new_r6))
            await client.send_message(message.channel,'Updated rank for P7: '+str(new_r7))
            await client.send_message(message.channel,'Updated rank for P8: '+str(new_r8))
            await client.send_message(message.channel,'Updated rank for P7: '+str(new_r9))
            await client.send_message(message.channel,'Updated rank for P8: '+str(new_r10))

            
            r1s = new_r1.sigma
            r2s = new_r2.sigma
            r3s = new_r3.sigma
            r4s = new_r4.sigma
            r5s = new_r5.sigma
            r6s = new_r6.sigma
            r7s = new_r7.sigma
            r8s = new_r8.sigma
            r9s = new_r9.sigma
            r10s = new_r10.sigma
            r1m = new_r1.mu
            r2m = new_r2.mu
            r3m = new_r3.mu
            r4m = new_r4.mu
            r5m = new_r5.mu
            r6m = new_r6.mu
            r7m = new_r7.mu
            r8m = new_r8.mu
            r9m = new_r9.mu
            r10m = new_r10.mu
         

            db.child("players").child(xp1.content).update({"mu": r1m})
            db.child("players").child(xp1.content).update({"sigma":r1s})
            db.child("players").child(xp2.content).update({"mu": r2m})
            db.child("players").child(xp2.content).update({"sigma":r2s})
            db.child("players").child(xp3.content).update({"mu": r3m})
            db.child("players").child(xp3.content).update({"sigma":r3s})
            db.child("players").child(xp4.content).update({"mu": r4m})
            db.child("players").child(xp4.content).update({"sigma":r4s})
            
            db.child("players").child(xp5.content).update({"mu": r5m})
            db.child("players").child(xp5.content).update({"sigma":r5s})
            db.child("players").child(xp6.content).update({"mu": r6m})
            db.child("players").child(xp6.content).update({"sigma":r6s})
            db.child("players").child(xp7.content).update({"mu": r7m})
            db.child("players").child(xp7.content).update({"sigma":r7s})
            db.child("players").child(xp8.content).update({"mu": r8m})
            db.child("players").child(xp8.content).update({"sigma":r8s})
            
            db.child("players").child(xp7.content).update({"mu": r9m})
            db.child("players").child(xp7.content).update({"sigma":r9s})
            db.child("players").child(xp8.content).update({"mu": r10m})
            db.child("players").child(xp8.content).update({"sigma":r10s})

        #find players
        elif message.content.startswith('.find'):
            await client.send_message(message.channel,'what art thou searcheth for:')
            xp1 = await client.wait_for_message(author=message.author)
            users = db.child("players").child(xp1.content).get()
            x=users.val()
            try:
                await client.send_message(message.channel,x)
            except discord.errors.HTTPException:
                await client.send_message(message.channel,'Player not found')
        #coinflip
        elif message.content.startswith('coinflip'):        
            tails = 0
            heads = 0
            flip = 0

            while flip < 100:
                fliparoo = random.randrange(2)
                if fliparoo == 0:
                    tails = tails + 1
                else:
                    heads = heads + 1
                flip += 1

            if heads>tails:
                await client.send_message(message.channel,'heads: '+str(heads))
            else:
                await client.send_message(message.channel,'tails: '+str(tails))
        
        #ordered list of players  
        elif message.content.startswith('player.list'):
            await client.send_message(message.channel,'big ass message incoming')
            users = db.child("players").get()
            x = users.val()
            playerfile=open("players.txt","w")
            playerfile.write(str(x))
            playerfile.close()
            await client.send_file(message.channel,"players.txt")
            
        elif message.content.startswith('n.players'):
            await client.send_message(message.channel, '`how many?`')
            amount_of_players = await client.wait_for_message(author=message.author)
            for i in range(int(amount_of_players.content)):
                xp3 = await client.wait_for_message(author=message.author)
                await client.send_message(message.channel, '`pushing data`')
                db.child("players").child(xp3.content).child("mu").set(10)
                db.child("players").child(xp3.content).child("sigma").set(8)

        elif message.content.upper().startswith('~help'):
            await client.send_message(message.channel,'```player_list' + "\n" + 'coinflip' + "\n" + "find" + "\n" + "set_major_role_perm" + "\n" + "set_minor_role_perm" + "\n" + "update_major_role_perm" + "\n" + "update_minor_role_perm```")
                

        elif message.content.upper().startswith('~set_major_role_perm'):
            await client.send_message(message.channel, "What role would you like to access the bot's admin functions?")
            major_access = await client.wait_for_message(author=message.author)
            db.child("major_role").set(major_access.content)
            

        elif message.content.upper().startswith('~set_minor_role_perm'):
            await client.send_message(message.channel, "What role would you like to access the bot's lesser functions?")
            minor_access = await client.wait_for_message(author=message.author)
            db.child("minor_role").set(minor_access)

        elif message.content.upper().startswith('~update_major_role_perm'):
            await client.send_message(message.channel, "What role would you like to access the bot's admin functions?")
            major_access = await client.wait_for_message(author=message.author)
            db.child("major_role").update(major_access.content)

        elif message.content.upper().startswith('~update_minor_role_perm'):
            await client.send_message(message.channel, "What role would you like to access the bot's lesser functions?")
            minor_access = await client.wait_for_message(author=message.author)
            db.child("minor_role").update(minor_access.content)
                      



client.run("") #token
