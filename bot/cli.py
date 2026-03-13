#!/usr/bin/env python3
import argparse
import sys
from bot import validators
from bot import orders
from bot.logging_config import setup_logging

def main():
    # Setup logging (logs will go to trading_bot.log)
    setup_logging("trading_bot.log")

    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")
    parser.add_argument("--symbol", required=True, help="Trading pair, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"], help="Order side")
    parser.add_argument("--type", required=True, choices=["MARKET", "LIMIT"], dest="order_type", help="Order type")
    parser.add_argument("--quantity", required=True, help="Quantity to trade")
    parser.add_argument("--price", help="Required for LIMIT orders")

    args = parser.parse_args()

    # Validate inputs
    if not validators.validate_symbol(args.symbol):
        print("Error: Invalid symbol format. Should be like 'BTCUSDT'.", file=sys.stderr)
        sys.exit(1)
    if not validators.validate_side(args.side):
        print("Error: Side must be BUY or SELL.", file=sys.stderr)
        sys.exit(1)
    if not validators.validate_order_type(args.order_type):
        print("Error: Order type must be MARKET or LIMIT.", file=sys.stderr)
        sys.exit(1)
    if not validators.validate_quantity(args.quantity):
        print("Error: Quantity must be a positive number.", file=sys.stderr)
        sys.exit(1)
    if args.order_type == "LIMIT":
        if not args.price:
            print("Error: Price is required for LIMIT orders.", file=sys.stderr)
            sys.exit(1)
        if not validators.validate_price(args.price):
            print("Error: Price must be a positive number.", file=sys.stderr)
            sys.exit(1)

    # Prepare order params for summary
    params = {
        "symbol": args.symbol,
        "side": args.side,
        "type": args.order_type,
        "quantity": args.quantity,
    }
    if args.price:
        params["price"] = args.price

    orders.print_order_summary(params)

    try:
        response = orders.place_order(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=float(args.quantity),
            price=float(args.price) if args.price else None
        )
        orders.print_order_response(response)
        print("SUCCESS: Order placed successfully.")
    except Exception as e:
        print(f"FAILURE: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()