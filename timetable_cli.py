from timetable import Timetable

import click

# reformat using OOP desing model

t = Timetable()

def parse_days(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    value_list = [x.strip() for x in value.split(",")]
    return value_list


@click.group(invoke_without_command=True)
@click.pass_context
@click.option("--days", "-d", type=str, default=None, callback=parse_days, help="Get timetable for day(s)")
def cli(ctx, days):
    """
    [Description]
    A command line timetable utility created with python. 
    A fun project to explore python language, click and rich
    packages. 
    """
    # add some validation checking for the existence of a timetable.csv or fn
    if ctx.invoked_subcommand is None:
        t.view_day(days)


@cli.command()
@click.option(
    "--filename",
    "-f",
    "fn",
    type=str,
    default=None,
    help="pass in csv filename to save timetable content",
)
def set(fn):
    """ 
    Creates a new timetable file 
    options : 
        -f/--filename [filename]  saves newly created timetable in filename 
    """
    t.filename = fn
    t.set_timetable()


@cli.command()
@click.option('--day', '-day', type=str, callback=parse_days, required=True)
def reset(day):
    """
    Cleans and write a new timetable contents for 
    a specified day
    """
    t.reset_day(d)

@cli.command()
def showtable():
    """
    Prints out the table on screen
    """
    if not t._table:
        t.load_table()
    t.print_table()


if __name__ == "__main__":
    cli()
