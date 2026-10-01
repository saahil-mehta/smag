# Generated images: prompts and provenance

Generated with the Codex CLI image tool for pages with no matching SMAG
photograph. They are generic industrial scenes and show no SMAG product.

| File | Used on |
| --- | --- |
| `oil-gas-banner-master.png` | /industries/oil-and-gas/ banner (renditions `site/site/assets/images/smag/oil-and-gas-banner.*.jpg`) |
| `brochure-stills/scene-black-powder.png` | How Black Powder Forms, guide card |
| `brochure-stills/scene-cnc-coolant.png` | What Does a Coolant Filter Do?, guide card |
| `brochure-stills/scene-cnc-workshop.png` | Types of Filtration for CNC Machines, guide card |
| `brochure-stills/scene-steel-plate-stock.png` | Hidden Costs of Traditional Steel Lifting, guide card |
| `brochure-stills/scene-chain-sling-lift.png` | Why Magnetic Lifters Are More Efficient than Chains and Slings, guide card |

The brochure-stills copies are centre crops to the 315:247 card shape.
`tools/rebuild/sync_guide_cards.py` renders and wires the cards.

## Prompts

Rules for every image:
- Photorealistic industrial photography, natural colour, sharp focus, professional commercial look, like a stock photo for an Indian engineering manufacturer's website.
- No text, letters, numbers, signage, logos, brand names, labels or watermarks anywhere in the frame.
- No recognisable faces. People, if any, are small, in the distance, or seen from behind, wearing proper PPE (hard hat, hi-vis, gloves).
- Main subject centred horizontally with calm space at the left and right, because the image will be cropped to different shapes.

1. oil-gas-banner.png
   A natural gas gathering and filtration station on a clear morning. Above-ground grey and silver steel pipelines run across the frame on concrete supports, with large flanges, gate valves and a vertical pressure vessel. Gravel ground, a perimeter fence in the far distance, soft sky. Wide establishing shot, horizon low in the frame.

2. scene-black-powder.png
   Close-up of a short section of steel gas pipe that has been cut open lengthways, lying on a workshop bench. The inside wall is coated with a fine, dark grey-black powder deposit and patches of rust-brown corrosion. Shallow depth of field, neutral grey background.

3. scene-cnc-coolant.png
   Inside a CNC milling machine during cutting: a carbide end mill cutting a steel block, milky white coolant flooding over the cutter from a flexible nozzle, small bright metal chips flying. Seen through the open machine door, cool workshop light.

4. scene-cnc-workshop.png
   A clean, bright machine shop with a row of modern CNC machining centres along one side, each with its coolant tank at the base, and a painted walkway down the middle. Wide shot, no people or one distant operator from behind.

5. scene-chain-sling-lift.png
   An overhead gantry crane in a steel stockyard lifting a stack of thick steel plates using steel chains and hooks at the corners, the chains taut. One rigger in hi-vis and hard hat stands at a safe distance, seen from behind. Industrial shed with high roof, daylight from the side.


6. scene-steel-plate-stock.png
   A steel service centre: tall neat stacks of thick hot-rolled steel plates on timber bearers, a yellow overhead crane beam high above, a forklift in the far background. Wide shot, daylight through high windows, main subject centred with calm space left and right.

## Gemini batch (1 Oct 2026): Eclipse images replaced

Generated in the Gemini web app (Nano Banana, Ultra plan) through the
automated browser. Each Eclipse image was uploaded as a brief for subject and
mood only, with a prompt asking for a new, original image with no text or
logos. Masters are in `assets/source/generated/`. They were written over every
rendition of the Eclipse asset with `tools/rebuild/replace_eclipse_images.py`,
so no HTML changed. Product photos carry the S-MAG watermark; scenes do not.

| Asset folder (`site/site/assets/files/`) | Master |
| --- | --- |
| 2023, 1079 aerospace banner, tile | `generated/2023-aerospace.jpg` |
| 2027, 1080 pharma | `generated/2027-pharma.jpg` |
| 2029, 1081 steel | `generated/2029-steel.jpg` |
| 2035, 1083 food | `generated/2035-food.jpg` |
| 2219, 2217 chemical | `generated/2219-chemical.jpg` |
| 2225, 2223 plastics | `generated/2225-plastics.jpg` |
| 2233, 2231 sugar | `generated/2233-sugar.jpg` |
| 1224, 33685 industries and home banner | `generated/1224-industries.jpg` |
| 33681 home filtration banner | `generated/33681-home-filtration.jpg` |
| 35079 guides banner | `generated/35079-guides.jpg` |
| 1241, 1151, 1143, 1329 family banners | `generated/still-*-wide.jpg`: SMAG's own `product-stills/` photos, zoomed out by Gemini |
| 1148 workholding banner | `product-stills/chucks-wide.jpg`: SMAG's chuck photo, background widened locally |
| 35874, 35880 pipeline banner, oil and gas tile | `oil-gas-banner-master.png` (Codex) |
| 10002 11299 3452 35852 35926 35932 36402 6422 6509 6812 8363 8471 9445 products | `generated/<folder>-product.jpg` (35926 uses 35852) |
| `brochure-stills/rectangular-magnetic-chuck-02.png` (Eclipse-labelled) | `generated/rectangular-magnetic-chuck-02-new.jpg` |

The product photos show generic versions of each product type, not SMAG's
own units. Check them against what SMAG makes before treating them as final.

### `generated/2029-steel.jpg`

Reference: `2029.jpg`. Aspect 16:9.

The attached photo belongs to another company. Use it only as a brief for the subject and mood. Create a new, original photograph: do not reproduce its composition, people, objects or any detail. Subject: Inside a steel stockholder's shed: rows of structural steel beams and thick plates on the floor, an overhead crane beam above, daylight through high windows. One single continuous photograph in one frame, never a collage, split panel or triptych. Wide 16:9 landscape. Keep the main subject near the middle of the frame with open space around it, because the photo will be cropped to a very wide banner and to a portrait. Photorealistic professional industrial photography, natural colour, sharp focus. Setting plausible for a factory in India. No text, letters, numbers, signage, logos, brand names, labels or watermarks anywhere in the image. No recognisable faces: any people are small, seen from the side or behind, wearing proper PPE.

### `generated/2023-aerospace.jpg`

Reference: `2023.jpg`. Aspect 16:9.

The attached photo belongs to another company. Use it only as a brief for the subject and mood. Create a new, original photograph: do not reproduce its composition, people, objects or any detail. Subject: An aircraft maintenance hangar: a commercial jet with an engine cowling open, two small engineers in hi-vis seen from behind at a workbench of precision machined parts in the middle distance; the aircraft is the main subject. One single continuous photograph in one frame, never a collage, split panel or triptych. Wide 16:9 landscape. Keep the main subject near the middle of the frame with open space around it, because the photo will be cropped to a very wide banner and to a portrait. Photorealistic professional industrial photography, natural colour, sharp focus. Setting plausible for a factory in India. No text, letters, numbers, signage, logos, brand names, labels or watermarks anywhere in the image. No recognisable faces: any people are small, seen from the side or behind, wearing proper PPE.

### `generated/2027-pharma.jpg`

Reference: `2027.jpg`. Aspect 16:9.

The attached photo belongs to another company. Use it only as a brief for the subject and mood. Create a new, original photograph: do not reproduce its composition, people, objects or any detail. Subject: A pharmaceutical tablet production clean room: a stainless steel tablet press and a conveyor carrying white tablets, an operator in full cleanroom gown, hood and mask. One single continuous photograph in one frame, never a collage, split panel or triptych. Wide 16:9 landscape. Keep the main subject near the middle of the frame with open space around it, because the photo will be cropped to a very wide banner and to a portrait. Photorealistic professional industrial photography, natural colour, sharp focus. Setting plausible for a factory in India. No text, letters, numbers, signage, logos, brand names, labels or watermarks anywhere in the image. No recognisable faces: any people are small, seen from the side or behind, wearing proper PPE.

### `generated/2035-food.jpg`

Reference: `2035.jpg`. Aspect 16:9.

The attached photo belongs to another company. Use it only as a brief for the subject and mood. Create a new, original photograph: do not reproduce its composition, people, objects or any detail. Subject: A food factory biscuit line: rows of golden baked biscuits on a stainless steel conveyor, a worker in hairnet and gloves checking them, bright hygienic light. One single continuous photograph in one frame, never a collage, split panel or triptych. Wide 16:9 landscape. Keep the main subject near the middle of the frame with open space around it, because the photo will be cropped to a very wide banner and to a portrait. Photorealistic professional industrial photography, natural colour, sharp focus. Setting plausible for a factory in India. No text, letters, numbers, signage, logos, brand names, labels or watermarks anywhere in the image. No recognisable faces: any people are small, seen from the side or behind, wearing proper PPE.

### `generated/2219-chemical.jpg`

Reference: `2219.jpg`. Aspect 16:9.

The attached photo belongs to another company. Use it only as a brief for the subject and mood. Create a new, original photograph: do not reproduce its composition, people, objects or any detail. Subject: A chemical processing plant: stainless steel reactor vessels, pipework and a powder dosing line, an operator in coveralls and safety glasses checking a gauge. One single continuous photograph in one frame, never a collage, split panel or triptych. Wide 16:9 landscape. Keep the main subject near the middle of the frame with open space around it, because the photo will be cropped to a very wide banner and to a portrait. Photorealistic professional industrial photography, natural colour, sharp focus. Setting plausible for a factory in India. No text, letters, numbers, signage, logos, brand names, labels or watermarks anywhere in the image. No recognisable faces: any people are small, seen from the side or behind, wearing proper PPE.

### `generated/2225-plastics.jpg`

Reference: `2225.jpg`. Aspect 16:9.

The attached photo belongs to another company. Use it only as a brief for the subject and mood. Create a new, original photograph: do not reproduce its composition, people, objects or any detail. Subject: Close up of plastic granules and recycled plastic flakes pouring from a hopper into a stainless steel chute in a plastics processing plant. One single continuous photograph in one frame, never a collage, split panel or triptych. Wide 16:9 landscape. Keep the main subject near the middle of the frame with open space around it, because the photo will be cropped to a very wide banner and to a portrait. Photorealistic professional industrial photography, natural colour, sharp focus. Setting plausible for a factory in India. No text, letters, numbers, signage, logos, brand names, labels or watermarks anywhere in the image. No recognisable faces: any people are small, seen from the side or behind, wearing proper PPE.

### `generated/2233-sugar.jpg`

Reference: `2233.jpg`. Aspect 16:9.

The attached photo belongs to another company. Use it only as a brief for the subject and mood. Create a new, original photograph: do not reproduce its composition, people, objects or any detail. Subject: A sugar mill processing hall: a stainless steel conveyor carrying white crystal sugar, centrifuges and pipework behind, warm industrial light. One single continuous photograph in one frame, never a collage, split panel or triptych. Wide 16:9 landscape. Keep the main subject near the middle of the frame with open space around it, because the photo will be cropped to a very wide banner and to a portrait. Photorealistic professional industrial photography, natural colour, sharp focus. Setting plausible for a factory in India. No text, letters, numbers, signage, logos, brand names, labels or watermarks anywhere in the image. No recognisable faces: any people are small, seen from the side or behind, wearing proper PPE.

### `generated/1224-industries.jpg`

Reference: `1224.jpg`. Aspect 16:9.

The attached photo belongs to another company. Use it only as a brief for the subject and mood. Create a new, original photograph: do not reproduce its composition, people, objects or any detail. Subject: A wide view of a modern Indian manufacturing plant floor with several kinds of process lines, conveyors and machinery, engineers walking in the distance. One single continuous photograph in one frame, never a collage, split panel or triptych. Wide 16:9 landscape. Keep the main subject near the middle of the frame with open space around it, because the photo will be cropped to a very wide banner and to a portrait. Photorealistic professional industrial photography, natural colour, sharp focus. Setting plausible for a factory in India. No text, letters, numbers, signage, logos, brand names, labels or watermarks anywhere in the image. No recognisable faces: any people are small, seen from the side or behind, wearing proper PPE.

### `generated/33681-home-filtration.jpg`

Reference: `33681.jpg`. Aspect 16:9.

The attached photo belongs to another company. Use it only as a brief for the subject and mood. Create a new, original photograph: do not reproduce its composition, people, objects or any detail. Subject: A CNC machine shop: a stainless steel magnetic filter unit plumbed into a machine tool coolant line, milky coolant flowing, machined steel parts nearby. One single continuous photograph in one frame, never a collage, split panel or triptych. Wide 16:9 landscape. Keep the main subject near the middle of the frame with open space around it, because the photo will be cropped to a very wide banner and to a portrait. Photorealistic professional industrial photography, natural colour, sharp focus. Setting plausible for a factory in India. No text, letters, numbers, signage, logos, brand names, labels or watermarks anywhere in the image. No recognisable faces: any people are small, seen from the side or behind, wearing proper PPE.

### `generated/35079-guides.jpg`

Reference: `35079.png`. Aspect 16:9.

The attached photo belongs to another company. Use it only as a brief for the subject and mood. Create a new, original photograph: do not reproduce its composition, people, objects or any detail. Subject: An engineer's workbench in a factory office: printed technical drawings, a steel rule, a few industrial magnets and a hard hat, soft window light, shallow depth of field. One single continuous photograph in one frame, never a collage, split panel or triptych. Wide 16:9 landscape. Keep the main subject near the middle of the frame with open space around it, because the photo will be cropped to a very wide banner and to a portrait. Photorealistic professional industrial photography, natural colour, sharp focus. Setting plausible for a factory in India. No text, letters, numbers, signage, logos, brand names, labels or watermarks anywhere in the image. No recognisable faces: any people are small, seen from the side or behind, wearing proper PPE.

### `generated/10002-product.jpg`

Reference: `10002.jpg`. Aspect 4:3.

The attached photo shows another company's product. Use it only as a guide to what kind of product this is. Create a new, original studio product photograph of a generic version: do not copy its exact design, angle or details. Subject: A neodymium channel magnet: a long U-shaped zinc-plated steel channel with a flat rectangular neodymium magnet set inside it and two countersunk mounting holes. Photorealistic industrial product photograph, centred on a seamless pure white studio background with a soft natural contact shadow, softbox lighting, three-quarter view from slightly above, sharp focus, realistic fabrication detail such as weld seams and machining marks. One single photograph, not a collage. No text, labels, nameplates, logos, stickers or watermarks anywhere. No people.

### `generated/11299-product.jpg`

Reference: `11299.png`. Aspect 4:3.

The attached photo shows another company's product. Use it only as a guide to what kind of product this is. Create a new, original studio product photograph of a generic version: do not copy its exact design, angle or details. Subject: A circular permanent magnetic chuck for a grinding machine: a round steel body with a fine concentric pole pattern on its top face and a removable side lever handle. Photorealistic industrial product photograph, centred on a seamless pure white studio background with a soft natural contact shadow, softbox lighting, three-quarter view from slightly above, sharp focus, realistic fabrication detail such as weld seams and machining marks. One single photograph, not a collage. No text, labels, nameplates, logos, stickers or watermarks anywhere. No people.

### `generated/3452-product.jpg`

Reference: `3452.jpg`. Aspect 4:3.

The attached photo shows another company's product. Use it only as a guide to what kind of product this is. Create a new, original studio product photograph of a generic version: do not copy its exact design, angle or details. Subject: A square magnetic separation grid: a square polished stainless steel frame holding two staggered rows of polished stainless steel magnetic tubes. Photorealistic industrial product photograph, centred on a seamless pure white studio background with a soft natural contact shadow, softbox lighting, three-quarter view from slightly above, sharp focus, realistic fabrication detail such as weld seams and machining marks. One single photograph, not a collage. No text, labels, nameplates, logos, stickers or watermarks anywhere. No people.

### `generated/35852-product.jpg`

Reference: `35852.jpg`. Aspect 16:9.

The attached photo shows another company's product. Use it only as a guide to what kind of product this is. Create a new, original studio product photograph of a generic version: do not copy its exact design, angle or details. Subject: A modular high pressure magnetic pipeline filter installed at a gas plant: a large grey painted carbon steel pressure vessel on a skid with flanged inlet and outlet pipework and a bolted top closure, outdoors in daylight. Photorealistic industrial photography, natural daylight, sharp. One single photograph, not a collage. No text, labels, nameplates, placards, logos or watermarks anywhere. No recognisable faces.

### `generated/35932-product.jpg`

Reference: `35932.jpg`. Aspect 4:3.

The attached photo shows another company's product. Use it only as a guide to what kind of product this is. Create a new, original studio product photograph of a generic version: do not copy its exact design, angle or details. Subject: An inline magnetic pipeline filter: a polished stainless steel cylindrical housing with flanged side inlet and outlet and a bolted lid with lifting eye. Photorealistic industrial product photograph, centred on a seamless pure white studio background with a soft natural contact shadow, softbox lighting, three-quarter view from slightly above, sharp focus, realistic fabrication detail such as weld seams and machining marks. One single photograph, not a collage. No text, labels, nameplates, logos, stickers or watermarks anywhere. No people.

### `generated/36402-product.jpg`

Reference: `36402.jpg`. Aspect 4:3.

The attached photo shows another company's product. Use it only as a guide to what kind of product this is. Create a new, original studio product photograph of a generic version: do not copy its exact design, angle or details. Subject: A rectangular permanent magnetic chuck for a surface grinder: a rectangular steel body with a fine transverse pole pitch top plate of thin brass and steel strips, and a removable lever handle. Photorealistic industrial product photograph, centred on a seamless pure white studio background with a soft natural contact shadow, softbox lighting, three-quarter view from slightly above, sharp focus, realistic fabrication detail such as weld seams and machining marks. One single photograph, not a collage. No text, labels, nameplates, logos, stickers or watermarks anywhere. No people.

### `generated/6422-product.jpg`

Reference: `6422.jpg`. Aspect 4:3.

The attached photo shows another company's product. Use it only as a guide to what kind of product this is. Create a new, original studio product photograph of a generic version: do not copy its exact design, angle or details. Subject: An easy clean magnetic grid separator: a stainless steel frame holding a row of magnetic tubes, with thin stainless sleeves that slide off the tubes for cleaning. Photorealistic industrial product photograph, centred on a seamless pure white studio background with a soft natural contact shadow, softbox lighting, three-quarter view from slightly above, sharp focus, realistic fabrication detail such as weld seams and machining marks. One single photograph, not a collage. No text, labels, nameplates, logos, stickers or watermarks anywhere. No people.

### `generated/6509-product.jpg`

Reference: `6509.jpeg`. Aspect 4:3.

The attached photo shows another company's product. Use it only as a guide to what kind of product this is. Create a new, original studio product photograph of a generic version: do not copy its exact design, angle or details. Subject: A housed easy clean grid magnet: a square stainless steel housing with square inlet and outlet flanges and a drawer of magnetic tubes pulled half out. Photorealistic industrial product photograph, centred on a seamless pure white studio background with a soft natural contact shadow, softbox lighting, three-quarter view from slightly above, sharp focus, realistic fabrication detail such as weld seams and machining marks. One single photograph, not a collage. No text, labels, nameplates, logos, stickers or watermarks anywhere. No people.

### `generated/6812-product.jpg`

Reference: `6812.jpg`. Aspect 4:3.

The attached photo shows another company's product. Use it only as a guide to what kind of product this is. Create a new, original studio product photograph of a generic version: do not copy its exact design, angle or details. Subject: Two magnetic coolant filter units for machine tools: cylindrical stainless steel vessels with inlet and outlet pipes, a top lid and small stands. Photorealistic industrial product photograph, centred on a seamless pure white studio background with a soft natural contact shadow, softbox lighting, three-quarter view from slightly above, sharp focus, realistic fabrication detail such as weld seams and machining marks. One single photograph, not a collage. No text, labels, nameplates, logos, stickers or watermarks anywhere. No people.

### `generated/8363-product.jpg`

Reference: `8363.jpg`. Aspect 4:3.

The attached photo shows another company's product. Use it only as a guide to what kind of product this is. Create a new, original studio product photograph of a generic version: do not copy its exact design, angle or details. Subject: A small stack and a scatter of nickel plated neodymium disc magnets in several diameters. Photorealistic industrial product photograph, centred on a seamless pure white studio background with a soft natural contact shadow, softbox lighting, three-quarter view from slightly above, sharp focus, realistic fabrication detail such as weld seams and machining marks. One single photograph, not a collage. No text, labels, nameplates, logos, stickers or watermarks anywhere. No people.

### `generated/8471-product.jpg`

Reference: `8471.jpg`. Aspect 4:3.

The attached photo shows another company's product. Use it only as a guide to what kind of product this is. Create a new, original studio product photograph of a generic version: do not copy its exact design, angle or details. Subject: Nickel plated neodymium block magnets: rectangular bars in several sizes, a few stacked. Photorealistic industrial product photograph, centred on a seamless pure white studio background with a soft natural contact shadow, softbox lighting, three-quarter view from slightly above, sharp focus, realistic fabrication detail such as weld seams and machining marks. One single photograph, not a collage. No text, labels, nameplates, logos, stickers or watermarks anywhere. No people.

### `generated/9445-product.jpg`

Reference: `9445.jpg`. Aspect 4:3.

The attached photo shows another company's product. Use it only as a guide to what kind of product this is. Create a new, original studio product photograph of a generic version: do not copy its exact design, angle or details. Subject: A circular magnetic grid for a vibratory sieve: a stainless steel ring with a parallel row of polished magnetic tubes across it. Photorealistic industrial product photograph, centred on a seamless pure white studio background with a soft natural contact shadow, softbox lighting, three-quarter view from slightly above, sharp focus, realistic fabrication detail such as weld seams and machining marks. One single photograph, not a collage. No text, labels, nameplates, logos, stickers or watermarks anywhere. No people.

### `generated/still-filters-wide.jpg`

Reference: `still-filters.jpg`. Aspect 16:9.

Edit the attached photo. Zoom out: make the product smaller so it fills only about 40 percent of the picture height, keep it centred, and extend the dark textured studio background and floor seamlessly all around it. Keep the product itself exactly as it is, unchanged. Add nothing else: no text, logos or extra objects. One single photograph.

### `generated/still-lifters-wide.jpg`

Reference: `still-lifters.jpg`. Aspect 16:9.

Edit the attached photo. Zoom out: make the product smaller so it fills only about 40 percent of the picture height, keep it centred, and extend the dark textured studio background and floor seamlessly all around it. Keep the product itself exactly as it is, unchanged. Add nothing else: no text, logos or extra objects. One single photograph.

### `generated/still-separators-wide.jpg`

Reference: `still-separators.jpg`. Aspect 16:9.

Edit the attached photo. Zoom out: make the product smaller so it fills only about 40 percent of the picture height, keep it centred, and extend the dark textured studio background and floor seamlessly all around it. Keep the product itself exactly as it is, unchanged. Add nothing else: no text, logos or extra objects. One single photograph.

### `generated/still-tools-wide.jpg`

Reference: `still-tools.jpg`. Aspect 16:9.

Edit the attached photo. Zoom out: make the product smaller so it fills only about 40 percent of the picture height, keep it centred, and extend the dark textured studio background and floor seamlessly all around it. Keep the product itself exactly as it is, unchanged. Add nothing else: no text, logos or extra objects. One single photograph.

### `generated/rectangular-magnetic-chuck-02-new.jpg`

Reference: `rectangular-magnetic-chuck-02.png`. Aspect 4:3.

The attached photo shows another company's product. Use it only as a guide to what kind of product this is. Create a new, original studio product photograph of a generic version: do not copy its exact design, angle or details. Subject: A rectangular permanent magnetic chuck for a surface grinder: a rectangular steel body with a fine transverse pole pitch top plate of thin brass and steel strips, and a removable lever handle. Photorealistic industrial product photograph, centred on a seamless pure white studio background with a soft natural contact shadow, softbox lighting, low front three-quarter view showing the long side of the chuck, with the lever handle lying on the white surface in front of it, sharp focus, realistic fabrication detail such as weld seams and machining marks. One single photograph, not a collage. No text, labels, nameplates, logos, stickers or watermarks anywhere. No people.
