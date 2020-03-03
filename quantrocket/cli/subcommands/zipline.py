# Copyright 2017 QuantRocket - All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
from quantrocket.cli.utils.parse import dict_str

def add_subparser(subparsers):
    _parser = subparsers.add_parser("zipline", description="QuantRocket CLI for Zipline", help="Backtest and trade Zipline strategies")
    _subparsers = _parser.add_subparsers(title="subcommands", dest="subcommand")
    _subparsers.required = True

    examples = """
Create a Zipline bundle for US stocks.

This command defines the bundle parameters but does not ingest the actual
data. To ingest the data, see `quantrocket zipline ingest`.


Examples:

Create a bundle named "usstock-1min":

    quantrocket zipline create-usstock-bundle usstock-1min
    """
    parser = _subparsers.add_parser(
        "create-usstock-bundle",
        help="create a Zipline bundle for US stocks",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "code",
        metavar="CODE",
        help="the code to assign to the bundle (lowercase alphanumerics and hyphens only)")
    parser.add_argument(
        "-u", "--universe",
        choices=["US", "FREE"],
        help="the universe to ingest. Possible choices: %(choices)s")
    parser.set_defaults(func="quantrocket.zipline._cli_create_usstock_bundle")

    examples = """
Create a Zipline bundle from a history database or real-time aggregate
database.

You can ingest 1-minute or 1-day databases.

This command defines the bundle parameters but does not ingest the actual
data. To ingest the data, see `quantrocket zipline ingest`.

Examples:

Create a bundle from a history database called "es-fut-1min" and name
it like the history database:

    quantrocket zipline create-db-bundle es-fut-1min --from-db es-fut-1min --calendar us_futures

Create a bundle named "usa-stk-1min-2017" for ingesting a single year of US
1-minute stock data from a history database called "usa-stk-1min":

    quantrocket zipline create-db-bundle usa-stk-1min-2017 --from-db usa-stk-1min -s 2017-01-01 -e 2017-12-31 --calendar XNYS
    """
    parser = _subparsers.add_parser(
        "create-db-bundle",
        help="create a Zipline bundle from a history database or real-time aggregate database",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "code",
        metavar="CODE",
        help="the code to assign to the bundle (lowercase alphanumerics and hyphens only)")
    parser.add_argument(
        "-d", "--from-db",
        metavar="CODE",
        help="the code of a history database or real-time aggregate database to ingest")
    parser.add_argument(
        "-c", "--calendar",
        metavar="NAME",
        help="the name of the calendar to use with this bundle "
        "(provide '?' or any invalid calendar name to see available choices)")
    parser.add_argument(
        "-f", "--fields",
        nargs="*",
        type=dict_str,
        metavar="ZIPLINE_FIELD:DB_FIELD",
        help="mapping of Zipline fields (open, high, low, close, volume) to "
        "db fields. Pass as 'zipline_field:db_field'. Defaults to mapping Zipline "
        "'open' to db 'Open', etc.")
    filters = parser.add_argument_group("filtering options for db ingestion")
    filters.add_argument(
        "-s", "--start-date",
        metavar="YYYY-MM-DD",
        help="limit to historical data on or after this date")
    filters.add_argument(
        "-e", "--end-date",
        metavar="YYYY-MM-DD",
        help="limit to historical data on or before this date")
    filters.add_argument(
        "-u", "--universes",
        nargs="*",
        metavar="UNIVERSE",
        help="limit to these universes")
    filters.add_argument(
        "-i", "--sids",
        nargs="*",
        metavar="SID",
        help="limit to these sids")
    filters.add_argument(
        "--exclude-universes",
        nargs="*",
        metavar="UNIVERSE",
        help="exclude these universes")
    filters.add_argument(
        "--exclude-sids",
        nargs="*",
        metavar="SID",
        help="exclude these sids")
    parser.set_defaults(func="quantrocket.zipline._cli_create_db_bundle")

    examples = """
Ingest data into a previously defined bundle.

Examples:

Ingest data into a bundle called es-fut-1min:

    quantrocket zipline ingest es-fut-1min
    """
    parser = _subparsers.add_parser(
        "ingest",
        help="ingest data into a previously defined bundle",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "code",
        metavar="CODE",
        help="the bundle code")
    parser.set_defaults(func="quantrocket.zipline._cli_ingest_bundle")

    examples = """
List available data bundles and whether data has been ingested into them.

Examples:

    quantrocket zipline list-bundles
    """
    parser = _subparsers.add_parser(
        "list-bundles",
        help="list available data bundles and whether data has been ingested into them",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.set_defaults(func="quantrocket.zipline._cli_list_bundles")

    examples = """
Delete a bundle.

Examples:

Delete a bundle called 'es-fut-1min':

    quantrocket zipline drop-bundle es-fut-1min --confirm-by-typing-bundle-code-again es-fut-1min
    """
    parser = _subparsers.add_parser(
        "drop-bundle",
        help="delete a bundle",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "code",
        metavar="CODE",
        help="the bundle code")
    parser.add_argument(
        "--confirm-by-typing-bundle-code-again",
        metavar="CODE",
        required=True,
        help="enter the bundle code again to confirm you want to drop the bundle, its config, "
        "and all its data")
    parser.set_defaults(func="quantrocket.zipline._cli_drop_bundle")

    examples = """
Backtest a Zipline strategy and write the test results to a CSV file.

The CSV result file contains several DataFrames stacked into one: the Zipline performance
results, plus the extracted returns, transactions, positions, and benchmark returns from those
results.

Examples:

Run a backtest from a strategy file called etf_arb.py and save a CSV file of results:

    quantrocket zipline backtest etf_arb.py --bundle arca-etf-eod -s 2010-04-01 -e 2016-02-01 -o results.csv
    """
    parser = _subparsers.add_parser(
        "backtest",
        help="backtest a Zipline strategy and write the test results to a CSV file",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "strategy",
        metavar="FILENAME",
        help="the file that contains the strategy to run")
    parser.add_argument(
        "--data-frequency",
        choices=["daily", "minute"],
        help="the data frequency of the simulation (default is daily)")
    parser.add_argument(
        "--capital-base",
        type=float,
        metavar="FLOAT",
        help="the starting capital for the simulation (default is 10000000.0)")
    parser.add_argument(
        "-b", "--bundle",
        metavar="BUNDLE-NAME",
        required=True,
        help="the data bundle to use for the simulation")
    parser.add_argument(
        "-s", "--start",
        required=True,
        metavar="DATE",
        help="the start date of the simulation")
    parser.add_argument(
        "-e", "--end",
        required=True,
        metavar="DATE",
        help="the end date of the simulation")
    parser.add_argument(
        "-o", "--output",
        metavar="FILENAME",
        dest="filepath_or_buffer",
        help="the location to write the output file (omit to write to stdout)")
    parser.set_defaults(func="quantrocket.zipline._cli_backtest")

    examples = """
Create a pyfolio PDF tear sheet from a Zipline backtest result.

Examples:

Create a pyfolio tear sheet from a Zipline CSV results file:

    quantrocket zipline tearsheet results.csv -o results.pdf

Run a Zipline backtest and create a pyfolio tear sheet without saving
the CSV file:

    quantrocket zipline backtest buy_aapl.py -s 2010-04-01 -e 2016-02-01 | quantrocket zipline tearsheet -o buy_aapl.pdf
    """
    parser = _subparsers.add_parser(
        "tearsheet",
        help="create a pyfolio tear sheet from a Zipline backtest result",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "infilepath_or_buffer",
        metavar="FILENAME",
        nargs="?",
        default="-",
        help="the CSV file from a Zipline backtest (omit to read file from stdin)")
    parser.add_argument(
        "-o", "--output",
        metavar="FILENAME",
        required=True,
        dest="outfilepath_or_buffer",
        help="the location to write the pyfolio tear sheet")
    parser.set_defaults(func="quantrocket.zipline._cli_create_tearsheet")

    examples = """
Trade a Zipline strategy.

Examples:

Trade a strategy:

    quantrocket zipline trade momentum_pipeline.py --bundle my-bundle
    """
    parser = _subparsers.add_parser(
        "trade",
        help="trade a Zipline strategy",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "strategy",
        metavar="FILENAME",
        help="the file that contains the strategy to run")
    parser.add_argument(
        "-b", "--bundle",
        metavar="BUNDLE-NAME",
        required=True,
        help="the data bundle to use")
    parser.add_argument(
        "-a", "--account",
        help="the account to run the strategy in. Only required "
        "if the strategy is allocated to more than one "
        "account in quantrocket.zipline.allocations.yml")
    parser.set_defaults(func="quantrocket.zipline._cli_trade")

    examples = """
List actively trading Zipline strategies.

Examples:

List strategies:

    quantrocket zipline active
    """
    parser = _subparsers.add_parser(
        "active",
        help="list actively trading Zipline strategies",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.set_defaults(func="quantrocket.zipline._cli_list_active_strategies")

    examples = """
Cancel actively trading strategies.

Examples:

Cancel a single strategy:

    quantrocket zipline cancel --strategies momentum_pipeline.py

Cancel all strategies:

    quantrocket zipline cancel --all
    """
    parser = _subparsers.add_parser(
        "cancel",
        help="cancel actively trading strategies",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "-s", "--strategies",
        nargs="*",
        metavar="FILENAME",
        help="limit to these strategies")
    parser.add_argument(
        "-a", "--accounts",
        metavar="ACCOUNT",
        nargs="*",
        help="limit to these accounts")
    parser.add_argument(
        "--all",
        action="store_true",
        dest="cancel_all",
        help="cancel all actively trading strategies")
    parser.set_defaults(func="quantrocket.zipline._cli_cancel_strategies")
