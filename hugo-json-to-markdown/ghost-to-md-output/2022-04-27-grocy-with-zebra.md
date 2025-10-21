---
title: Grocy with zebra
slug: grocy-with-zebra
date: 2022-04-27T15:57:48.000Z
date_updated: 2022-04-28T00:40:06.000Z
summary: Find out how I reduced food waste by using a zebra barcode scanner
---

> Right off the bat, this is written more of a brain dump, to help those who also use grocy with a zebra scanner

So those of you who don't know me personally, I've moved to my own apartment.

Whilst yes, this is pretty cool, at the same time I now have an entire kitchen to myself. Which poses the issue of having more cupboards than I know what to do with.

I've recently started using a self hosted app called `Grocy` which effectively, is a warehouse management system for your kitchen, with some added functionality.

The concept of Grocy is simple, how ever getting started takes **a lot** of work.

If you're deploying Grocy for the first time, I suggest you start with adding the quantity units, locations, groups and if you're feeling spicy, the shelf number in the shop. (I give my values later on)

Regardless, what grocy has to offer is the ability to know when you got food, how long it has in your kitchen, when it's past it's sell by date, and then the best feature is automatically generating a shopping list.

Some screenshots of Grocy
![](__GHOST_URL__/content/images/2022/04/image.png)
Here we can see that my Beef meatballs are set to be out of their `Best before date` in 5 days, where as my white bread has 3 more days to go.
![](__GHOST_URL__/content/images/2022/04/image-1.png)
Here is my weeks meal plan, showing that I don't have all the ingredients in stock to make my [Meatball Tomato soup](https://www.bbcgoodfood.com/recipes/meatball-tomato-soup) (Recipe linked)
![](__GHOST_URL__/content/images/2022/04/image-2.png)I've got no veg stock as tesco were sold out
Finally there's a Calendar section which shows food due, as well as chores
![](__GHOST_URL__/content/images/2022/04/image-3.png)
The cool part here is we're able to assign barcodes to items (Both a grocy generated one, as well as the code from the shop, so a UPC)
![](__GHOST_URL__/content/images/2022/04/image-4.png)
This is important to have, as it allows easy stock taking and purchasing, with my Zebra barcode scanner.

I'll share my values that I'm using for each section, in hope that it enables you to speed up deploying grocy:

### Quantity Units

- Bag
- Blister Pack
- Bottle
- Box
- Bunch
- Pack
- Pattie
- Piece
- Pill
- Sachet
- Slice
- Tin

### Product Groups

- Alcohol
- Breads
- Chips (I'm BRI'ISH)
- Crisps
- Fresh Produce
- Medical
- Pasta
- Rice
- Sauces
- Spices
- Sweets
- Tinned

### Custom Fields (User fields)

    entity: products
    Name: tescolocation
    caption: Tesco Location
    Type: text (Single line)

    entity: products
    name:vegan
    caption: Is vegan
    type: Checkbox

I'm using the tesco shelf location as the Tesco where I live is like no other, I can't find things to save my life. As I shop I scan the location code of the product as well as the barcode, which allows me to build shopping lists around items that are close by.

## Roll on the zebra scanner

Like I said, I have a zebra TC56DJ (Most shops use these) which I recently purchased.

The serotonin this thing produces when it beeps is just 🤌
![](__GHOST_URL__/content/images/2022/04/image-5.png)
For shopping I have my personal phone open with the Grocy shopping list, I mark an item as done then scan it in on the Zebra.

I would **love** it if Grocy automatically removed items from the shopping list once there's been a purchase of that item, that's on the list... Oh well

I will update the below each time I get stopped with my scanner and someone assumes I work there
ShopDate
---

### Specifics to allow the Barcode scanner to work well with Grocy

Under the app `DataWedge` , make a new profile by clicking the 3 dots at the top right.

Once the new profile has loaded, click `Associated apps`

Here select `com.android.chrome`

On the menu after, select the `*` - this means that any time you scan a barcode in Chrome, it will use the profile you've created.

By default the TC56 supports scanning the following barcodes:

- QR
- Data Matrix
- PDF417
- Grid Matric
- Aztec code
- All 1D barcodes
- Royal Mail 2D barcode
- The weird barcodes you get on post

This is by no means an exhaustive list of compatibility, it's a list of barcodes I could scan in my Apartment

## Config changes made

You can configure the scanner to send the enter key after each barcode, which is what I was using for about 3 hours before it **really** messed things up.

I've disabled this and now gone with the below grocy config options

    DefaultUserSetting('product_presets_default_due_days', -1);
    DefaultUserSetting('scan_mode_consume_enabled', true);
    DefaultUserSetting('scan_mode_purchase_enabled', true);
    Setting('BASE_URL', 'https://grocy.breadoven'); //fixed the api thinking it was on localhost due to reverse proxy

By setting the default scan mode to true, the scanner doesn't always send an enter and then exit the form when you still need to add more data

## Limits to the scanner

### Minimum barcode

Something I found quite funny was the **minimum barcode**you need for a read. I currently have this at 1.10mm from about 20cm away

### Distance

Max distance for a 46.68mm x 10.28mm barcode is about 57cm with no shadows
Max distance for a 46.68mm x 10.28mm barcode is about 46cm with no light

Where as a 2d barcode measuring roughly 59.88 x 59.88 was able to read from a distance of 1.16**m!**

Without sounding like a sales rep, this is not bad for a device released around 2017

---

## Issues faced

What would self hosted be without issues google won't help you with

Sometimes barcode would not scan in apps

Make new dwd profile and attach it to `com.android.chrome.*`

### Enter key needing to be set to fill data

Set the config.php and disable send enter on barcode read *(See code block under changes made)*

### Keyboard keeps popping up

The app to stop a keyboard popping up isn't on the play store, so download at your own risk

Once downloaded enable the keyboard in settings, and select it in chrome or grocy app.

[https://m.apkpure.com/null-input-method/com.apedroid.hwkeyboardhelperfree](https://m.apkpure.com/null-input-method/com.apedroid.hwkeyboardhelperfree)

---

Overall I am quite excited to have this, I plan on trying to build my own UI to enable faster workflows, but I'm not a developer so who knows :)
