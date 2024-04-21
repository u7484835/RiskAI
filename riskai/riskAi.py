import click























































@click.command(name="riskAI")
@click.option("b", "--blizzards", type=bool, default=False, prompt= "Does the gamemode have blizards enabled?", help="The gamemode settings specifying blizzards.")
@click.option("-f", "--fog", type=bool, default=False, prompt= "Does the gamemode have fog enabled?", help="The gamemode settings specifying fog.")
def main(blizzards : bool, fog : bool):
    # Handles CLI interactions implemented by click package
    print("this is main")
    
    
