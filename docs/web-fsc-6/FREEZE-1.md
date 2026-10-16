# WEB-FSC-6 freeze 1 (before integration)

- Frozen HEAD: `2f1e5b969c1deb9becc5d4563f8ee8c2fc0dc233` (branch web-fsc-6)
- sha256 of `git archive 2f1e5b969c1deb9becc5d4563f8ee8c2fc0dc233`: `7da9508056cf1ebf18a077cfc388e4aec2666b15a0eb179b53b8a6e3ff1b2a1f`
- sha256 of the casemodel.py output (`python3 scripts/casemodel.py --dump <dir>`, the 15 JSON files concatenated in name order): `812e4fd0e66ddbcc02a7ca4949b6ce97db22b7864ef42e62281c2f2d17e91cd9`
- Draft deploy: `6ad2064ab5927d22435b3caa` (https://6ad2064ab5927d22435b3caa--splendid-cannoli-80c225.netlify.app), from `git archive 2f1e5b969c1deb9becc5d4563f8ee8c2fc0dc233` with src/ and docs/ removed (main does not yet carry WEB-FSC-4's /src/* 404 rule)
- Draft checks: 23/23 built pages HTTP 200 with the expected H1; the 8 folded URLs, /src/, /src/pages/states/texas.html, /docs/ and /docs/web-fsc-6/CLOSE.md all 404
- Gates at the freeze: docs/web-fsc-6/GATES.txt (9 green; 7, 11, 12, 14 red and 9 pending, each on an integration step: WEB-FSC-4's scripts, sitemap and its other pages)

## sha256 of every file under src/ and data/cases/

```
c8ada8a1a5207d8afa8d3dca5aee550bd3cd40d555e59486d05686c222494b9a  data/cases/assisted-living-texas-hud.json
b5a8bc7984938685e614d8f7ed23a303109e968db91a7906981cddb2bf8eaf58  data/cases/auto-dealership-texas-sba.json
f725a0096d9b055dd15a1f533d23b3bf6098c78862e0120b2ff76d28be38156e  data/cases/car-wash-texas-sba.json
22232812729da6eea9b8b00f7e2b36249b1fa7e939166199689872fa15f1ec0d  data/cases/gas-station-alabama-sba.json
5f17313f43839ae51cf67b82180b926a402d49e508119c307e340dee71a4f58b  data/cases/gas-station-florida-sba.json
6d2b3c2709f81a6f680df6533bdacb57132298627d172953ead33b7a37ae8442  data/cases/gas-station-georgia-sba.json
8e1a4e03c128541da3df5e3017371d76ff60940e60746ec72a41277ad7c0375a  data/cases/gas-station-texas-sba.json
6b53784d22f8152333051bd59055bb9065f47e999ee75ae542f6108604b69d84  data/cases/gas-station-versailles-ohio-sba.json
9996214cae08bf658887586bea99969d10a32b50b2acafa2b1f7e4aa0c28d45d  data/cases/hotel-texas-sba.json
bd8fa1ff514967781f4458d2c50c065eb2506325d1f4cfb977092760f4e34f7c  data/cases/lodging-retreat-johnson-city-texas-sba.json
315a7d0008fab0d2760a53935b2d04324216638b8777681de557d3d061b55d1f  data/cases/meat-processing-texas-usda.json
59e87e6f6be71d7d471c00eae7df2e6f18b40512ad80d150e41b1c39083e0abb  data/cases/rv-boat-storage-texas-sba.json
2154c46b83f868470bd06ff545c58e205ca1d541cc1484269a09a52253531094  data/cases/rv-park-texas-usda.json
8fc580b8d09e875cfa24ee7584be222a527aa03c149ed33ba9857976f4638482  data/cases/travel-center-hankamer-texas-usda.json
1fef77af342b0a2b2db04a95b6a2c4b92c4cc03f3a4ddc6c4661b893802ba3b5  data/cases/truck-stop-texas-sba.json
58e7acfd88d57f3f4f2bab19daed8862f24b5cdf0a6ab3e8a162abd7a6ca8e26  src/README.md
4cf7a68156191d0570487f1e36fcba89e2be0f9df9cb518f8cdc466d24180f46  src/pages/asset-classes/gas-station-and-c-store.html
0a3ff7b1cd7a758f0bcaaa45fb4fe9ad47cc2c0f6648121ee49f0b0f1726e31f  src/pages/asset-classes/gas-station-and-c-store/ev-charging.html
65a77d72a455db5edb03f597ac0c5ab7ae19726440da912663b8c37405146386  src/pages/asset-classes/gas-station-and-c-store/interstate-highway.html
0cce311a5660447cffe3d96d14a02418a7a3b1f6bc5dca1a06f1810a9fd9c2d4  src/pages/case-studies/assisted-living-texas-hud.html
a73321039e8faab7b7282278469d5e24d7b8924fb574b84537e1278dab8d5b89  src/pages/case-studies/auto-dealership-texas-sba.html
c5c8b6ab0329af109caec1255a5218b477dc9182348d51a94c5d9523c80bea71  src/pages/case-studies/car-wash-texas-sba.html
d6d8adf06783cb4cf744dc904f945bdd4771170ed597ab8a1ac1060f020f0527  src/pages/case-studies/gas-station-alabama-sba.html
0b30aaf26fa4048335bbdefc0e1095577b662bd95a8dc88cb09d065048df0abe  src/pages/case-studies/gas-station-florida-sba.html
9881d31197984bada7be8a06223dd75af61b610ecc1ebc6dd15c5543fbf1d64a  src/pages/case-studies/gas-station-georgia-sba.html
75cdf2c9909d360da43153fdb2222d847c5418ad3227ba530bcb3fb81ffd565a  src/pages/case-studies/gas-station-texas-sba.html
26d7d154597967b503701e942ef682c5bf451d5980948a93337318e505f14654  src/pages/case-studies/gas-station-versailles-ohio-sba.html
4bac58690aab6f3659f1ebdbe17438a9d325643617504b63dab5ce183a097a42  src/pages/case-studies/hotel-texas-sba.html
e27edc60b3277579e8a415abc9eb0243e5902b7f59aa16aede4df655d0f14e2c  src/pages/case-studies/lodging-retreat-johnson-city-texas-sba.html
afa67f4277afa5aa941a76384632d0dcd51149dfd6fdeda2386c543fd3863360  src/pages/case-studies/meat-processing-texas-usda.html
333a1c060315bcaf7ef1748ffb379e72df93ad7ea05d0329f1bbd7ed29ce3c8a  src/pages/case-studies/rv-boat-storage-texas-sba.html
241e90105dae34188f29d3cdfa8279b283e99763ef5cfc8247b36415253555f3  src/pages/case-studies/rv-park-texas-usda.html
ff75977fb8b22ee1ff0cc37991b27ab4dd6a104a31d4d0a54a835ecb47156c6e  src/pages/case-studies/travel-center-hankamer-texas-usda.html
c166c4d2bc48c14e5badb752d1f66487da715004339445e55005c5a6becc6a24  src/pages/case-studies/truck-stop-texas-sba.html
1e42a429cb1fee7e8b953ff02d8fb972e153d11ee04b17c63c288a622d491c00  src/pages/states/texas.html
7720519718508bb4ff4a6f264818f3c6b6000157a76577dbf7d5949ada7ed65d  src/pages/states/texas/austin.html
8120944184a8dde3d75733ddaa449b7cdd7c88fdfbf653d1e33c8dd856d73d73  src/pages/states/texas/dallas-fort-worth.html
755aeff5da31b46dea122d9bc751fae8841a381920eb6a779265e9bfbd1c78a6  src/pages/states/texas/houston.html
ba31749bb1ad0968d3cf08c47841fc607741beb2a8131a5cdf9c2382b9ab46dc  src/pages/states/texas/san-antonio.html
f38979a50c8b9acc42719a78e3d7cf9da0e288965f7558bc0d84f31220593fd8  src/site.json
3a494be8f76d4eac12801ecb024b6bf439476eefaaa6a70b347641c67654265a  src/templates/base.html
a0098b948c537cea24ac346262b1c0f7d88143647e680ae499957077450465ec  src/templates/case.html
9639e7d6cbb8129366a5ddcbebbb34d5c677fd04a2dfa5f3b2789093b5ed3568  src/templates/hub.html
9639e7d6cbb8129366a5ddcbebbb34d5c677fd04a2dfa5f3b2789093b5ed3568  src/templates/metro.html
c8d4fa73c90a0098f2998a8e77942d81c0647fc827a802ded3e0d70aaaa85689  src/templates/partials/case-components.css
8489f1e38aee40748984c4a450fd2ebe0c24e2d3f126a033a10a014e8c6fb3b7  src/templates/partials/factory.css
dd2e9296fc13ed00405615fadabae630751513e7bd21db3c045900d89e32b211  src/templates/partials/footer.html
733a21258a0876967659e57b7f34708602205d1a56ec9420cc1fca277ee722df  src/templates/partials/header.html
38b354ffc769b0ace60957f2dc8e512cf083b1dc9e5f3b3f0868bd755a82b190  src/templates/partials/house-a.css
fed3c15b9baf9ee330becb66eeef78381495534d892875290958e521ca96f9ed  src/templates/partials/house-b.css
f02f88d6d417a3e13d740c8052524f0c1dbdb91181791389a9914e7c2373341c  src/templates/partials/script.html
9639e7d6cbb8129366a5ddcbebbb34d5c677fd04a2dfa5f3b2789093b5ed3568  src/templates/state.html
9639e7d6cbb8129366a5ddcbebbb34d5c677fd04a2dfa5f3b2789093b5ed3568  src/templates/subtype.html
```

## sha256 of each casemodel.py output file

```
9c88c4314380b5913ace33d58ddb75dda504617c619c77ab316497cd74cbba5c  assisted-living-texas-hud.json
3b71c76c7eeedc8226e3983cc53d1f8d6809c45974dde2a08f99e89d076380ce  auto-dealership-texas-sba.json
7afa9d6810066b850fc30e947019fa8e4f35f8d3e997693e6eb97b9e3763fcd2  car-wash-texas-sba.json
c61d3bfdfae5af737b1093411cce924f97f3ed9ac4492c51c0f966c2d5003fb5  gas-station-alabama-sba.json
97a7c40664ff3d28dddce0a8b253b77aa132d7b6722acccb91eaf3009982ec7f  gas-station-florida-sba.json
53c298dc098e9309821684274ce61c23d8f95a99fb7bf0ee221f479c96a1234a  gas-station-georgia-sba.json
3d7d3f2a4e60ab4a38d28b44761b8b4751040685c02af4cc379233c10ed9b284  gas-station-texas-sba.json
c5c883bce31aa9aa70fa4583af472061e19e546949cc51fd6c552ff43d148b50  gas-station-versailles-ohio-sba.json
49102da8448299902fbc878812c5abd873bcb04095e54a4c3aa7bbffc0c09dfb  hotel-texas-sba.json
821435c934a9c9a4bcf605fd6dcb0dd58f267078c16790bf8fbde7c6e14e3383  lodging-retreat-johnson-city-texas-sba.json
f003ca186c7eb10cd36c35e4e1d893348bab3f2fab98327701ffa71e1ecc9d36  meat-processing-texas-usda.json
81cb5b39a890d58372831a4e0241771ad2c639a8a34b1ed1eeeb6183bca86c4c  rv-boat-storage-texas-sba.json
fa0a13a067e89c650d26143523e109ea6bc9ff8d5ef9ba7c57126a294c0ad81d  rv-park-texas-usda.json
3b32c319d5424db23b0901301e326fa41044c0cbeae8899b9cf80de04f7f8987  travel-center-hankamer-texas-usda.json
08aace0aa265d1a61c328f2c9e02ed2b7ce3890d05465ac46ca826b7a665f826  truck-stop-texas-sba.json
```

## Draft check output

```
200 h1=match /states/texas/
200 h1=match /states/texas/houston/
200 h1=match /states/texas/dallas-fort-worth/
200 h1=match /states/texas/austin/
200 h1=match /states/texas/san-antonio/
200 h1=match /asset-classes/gas-station-and-c-store/
200 h1=match /asset-classes/gas-station-and-c-store/interstate-highway/
200 h1=match /asset-classes/gas-station-and-c-store/ev-charging/
200 h1=match /case-studies/gas-station-texas-sba/
200 h1=match /case-studies/gas-station-florida-sba/
200 h1=match /case-studies/gas-station-alabama-sba/
200 h1=match /case-studies/gas-station-georgia-sba/
200 h1=match /case-studies/gas-station-versailles-ohio-sba/
200 h1=match /case-studies/truck-stop-texas-sba/
200 h1=match /case-studies/hotel-texas-sba/
200 h1=match /case-studies/rv-park-texas-usda/
200 h1=match /case-studies/car-wash-texas-sba/
200 h1=match /case-studies/rv-boat-storage-texas-sba/
200 h1=match /case-studies/auto-dealership-texas-sba/
200 h1=match /case-studies/assisted-living-texas-hud/
200 h1=match /case-studies/meat-processing-texas-usda/
200 h1=match /case-studies/travel-center-hankamer-texas-usda/
200 h1=match /case-studies/lodging-retreat-johnson-city-texas-sba/
404 folded /states/texas/mcallen/
404 folded /states/texas/el-paso/
404 folded /states/texas/lubbock/
404 folded /states/texas/corpus-christi/
404 folded /asset-classes/gas-station-and-c-store/branded-fuel/
404 folded /asset-classes/gas-station-and-c-store/unbranded-independent/
404 folded /asset-classes/gas-station-and-c-store/convenience-no-fuel/
404 folded /asset-classes/gas-station-and-c-store/foodservice-qsr/
404 /src/
404 /src/pages/states/texas.html
404 /docs/web-fsc-6/CLOSE.md
404 /docs/
pilot pages 200 with matching H1: 23/23
```
