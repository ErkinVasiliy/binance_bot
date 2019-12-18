

#стакан
def depth(client):
    depth = client.get_order_book(symbol='AA')

    for ask in reversed(depth['asks'][0:10]):
        print(ask)

    print()

    for bid in depth['bids'][0:10]:
        print(bid)