# Access one of our Heroku databases.
#
# Put the name of the SQL file you want to run after -f,
# or leave out the -f option to get to the prompt.
#
# Explanation:
# http://stackoverflow.com/a/15266851/752601

# leadlabdemo.herokuapp.com
# Password: biVt6hxh44xZO07L2mo8ayPToT 

#psql -f -h ec2-23-21-185-168.compute-1.amazonaws.com -p 5432 -d d6fn203hpvucst -U tirhgmxhmdkkyu 


# goodnight-lead.herokuapp.com
# Password: 33hq86Yck8WI9bgy0CY9TvtgnF

psql -h ec2-54-83-14-68.compute-1.amazonaws.com -p 5432 -d d1is7f4le695fo -U bmjucqcekvlqrm
