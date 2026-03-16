# Coupon Classifier & Ranker

Ever stared at a bunch of coupons and had no idea which one is actually worth using?

"Flat Rs.150 cashback" vs "Upto Rs.500 cashback" — the second one sounds better, 
but is it really?

That's the problem I wanted to solve. I built a small ML project that reads coupon 
text, figures out what type of coupon it is, and predicts the real expected value 
you'll likely get from it. Then it ranks them so you always know which one to pick.

## What it does

You paste your coupons into the app, hit a button, and it tells you which one is 
actually the best deal — not just the one with the biggest number in it.

## Why I built this

I kept seeing "upto Rs.500 cashback" offers everywhere and always wondered how 
much you actually get from them. Turns out, not much. So I built something to 
figure that out automatically.

## How it works

It's two models working together — one classifies the coupon type (flat cashback, 
upto cashback, flat percent, upto percent), and the other predicts the real 
expected value after accounting for the uncertainty in "upto" offers. The final 
output is a ranked list of your coupons from best to worst.
