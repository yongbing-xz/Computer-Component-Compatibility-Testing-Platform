PRODUCTS = [
    # ==================== CPU (40款) ====================
    # Intel 6th-10th Gen (LGA1151)
    {"id":1,"title":"Intel Core i3-6100","brand":"Intel","category":"CPU","socket":"LGA1151","price":599,"rating":4.2,"stock":15,"specs":{"cores":"2核4线程","baseClock":"3.7GHz","tdp":"51W","process":"14nm","gen":"6th"}},
    {"id":2,"title":"Intel Core i5-6500","brand":"Intel","category":"CPU","socket":"LGA1151","price":1099,"rating":4.3,"stock":8,"specs":{"cores":"4核4线程","baseClock":"3.2GHz","tdp":"65W","process":"14nm","gen":"6th"}},
    {"id":3,"title":"Intel Core i7-6700","brand":"Intel","category":"CPU","socket":"LGA1151","price":1799,"rating":4.5,"stock":5,"specs":{"cores":"4核8线程","baseClock":"3.4GHz","tdp":"65W","process":"14nm","gen":"6th"}},
    {"id":4,"title":"Intel Core i5-7500","brand":"Intel","category":"CPU","socket":"LGA1151","price":1199,"rating":4.3,"stock":10,"specs":{"cores":"4核4线程","baseClock":"3.4GHz","tdp":"65W","process":"14nm","gen":"7th"}},
    {"id":5,"title":"Intel Core i7-7700","brand":"Intel","category":"CPU","socket":"LGA1151","price":1899,"rating":4.5,"stock":6,"specs":{"cores":"4核8线程","baseClock":"3.6GHz","tdp":"65W","process":"14nm","gen":"7th"}},
    # Intel 8th-9th Gen (LGA1151-2)
    {"id":6,"title":"Intel Core i3-8100","brand":"Intel","category":"CPU","socket":"LGA1151-2","price":699,"rating":4.3,"stock":12,"specs":{"cores":"4核4线程","baseClock":"3.6GHz","tdp":"65W","process":"14nm","gen":"8th"}},
    {"id":7,"title":"Intel Core i5-8400","brand":"Intel","category":"CPU","socket":"LGA1151-2","price":1299,"rating":4.5,"stock":9,"specs":{"cores":"6核6线程","baseClock":"2.8GHz","tdp":"65W","process":"14nm","gen":"8th"}},
    {"id":8,"title":"Intel Core i7-8700","brand":"Intel","category":"CPU","socket":"LGA1151-2","price":2099,"rating":4.6,"stock":7,"specs":{"cores":"6核12线程","baseClock":"3.2GHz","tdp":"65W","process":"14nm","gen":"8th"}},
    {"id":9,"title":"Intel Core i5-9400F","brand":"Intel","category":"CPU","socket":"LGA1151-2","price":999,"rating":4.4,"stock":20,"specs":{"cores":"6核6线程","baseClock":"2.9GHz","tdp":"65W","process":"14nm","gen":"9th"}},
    {"id":10,"title":"Intel Core i7-9700","brand":"Intel","category":"CPU","socket":"LGA1151-2","price":2299,"rating":4.5,"stock":6,"specs":{"cores":"8核8线程","baseClock":"3.0GHz","tdp":"65W","process":"14nm","gen":"9th"}},
    {"id":11,"title":"Intel Core i9-9900K","brand":"Intel","category":"CPU","socket":"LGA1151-2","price":3299,"rating":4.7,"stock":4,"specs":{"cores":"8核16线程","baseClock":"3.6GHz","tdp":"95W","process":"14nm","gen":"9th"}},
    # Intel 10th-11th Gen (LGA1200)
    {"id":12,"title":"Intel Core i3-10100","brand":"Intel","category":"CPU","socket":"LGA1200","price":799,"rating":4.4,"stock":18,"specs":{"cores":"4核8线程","baseClock":"3.6GHz","tdp":"65W","process":"14nm","gen":"10th"}},
    {"id":13,"title":"Intel Core i5-10400F","brand":"Intel","category":"CPU","socket":"LGA1200","price":999,"rating":4.5,"stock":25,"specs":{"cores":"6核12线程","baseClock":"2.9GHz","tdp":"65W","process":"14nm","gen":"10th"}},
    {"id":14,"title":"Intel Core i7-10700","brand":"Intel","category":"CPU","socket":"LGA1200","price":2199,"rating":4.6,"stock":8,"specs":{"cores":"8核16线程","baseClock":"2.9GHz","tdp":"65W","process":"14nm","gen":"10th"}},
    {"id":15,"title":"Intel Core i5-11400","brand":"Intel","category":"CPU","socket":"LGA1200","price":1099,"rating":4.5,"stock":15,"specs":{"cores":"6核12线程","baseClock":"2.6GHz","tdp":"65W","process":"14nm","gen":"11th"}},
    {"id":16,"title":"Intel Core i7-11700","brand":"Intel","category":"CPU","socket":"LGA1200","price":2399,"rating":4.5,"stock":7,"specs":{"cores":"8核16线程","baseClock":"2.5GHz","tdp":"65W","process":"14nm","gen":"11th"}},
    # Intel 12th-14th Gen (LGA1700)
    {"id":17,"title":"Intel Core i3-12100F","brand":"Intel","category":"CPU","socket":"LGA1700","price":599,"rating":4.5,"stock":30,"specs":{"cores":"4核8线程","baseClock":"3.3GHz","tdp":"58W","process":"Intel 7","gen":"12th"}},
    {"id":18,"title":"Intel Core i5-12400F","brand":"Intel","category":"CPU","socket":"LGA1700","price":999,"rating":4.7,"stock":35,"specs":{"cores":"6核12线程","baseClock":"2.5GHz","tdp":"65W","process":"Intel 7","gen":"12th"}},
    {"id":19,"title":"Intel Core i5-12600K","brand":"Intel","category":"CPU","socket":"LGA1700","price":1599,"rating":4.7,"stock":12,"specs":{"cores":"10核16线程","baseClock":"3.7GHz","tdp":"125W","process":"Intel 7","gen":"12th"}},
    {"id":20,"title":"Intel Core i7-12700K","brand":"Intel","category":"CPU","socket":"LGA1700","price":2299,"rating":4.8,"stock":10,"specs":{"cores":"12核20线程","baseClock":"3.6GHz","tdp":"125W","process":"Intel 7","gen":"12th"}},
    {"id":21,"title":"Intel Core i9-12900K","brand":"Intel","category":"CPU","socket":"LGA1700","price":3599,"rating":4.8,"stock":5,"specs":{"cores":"16核24线程","baseClock":"3.2GHz","tdp":"125W","process":"Intel 7","gen":"12th"}},
    {"id":22,"title":"Intel Core i5-13400F","brand":"Intel","category":"CPU","socket":"LGA1700","price":1199,"rating":4.6,"stock":28,"specs":{"cores":"10核16线程","baseClock":"2.5GHz","tdp":"65W","process":"Intel 7","gen":"13th"}},
    {"id":23,"title":"Intel Core i7-13700K","brand":"Intel","category":"CPU","socket":"LGA1700","price":2599,"rating":4.8,"stock":9,"specs":{"cores":"16核24线程","baseClock":"3.4GHz","tdp":"125W","process":"Intel 7","gen":"13th"}},
    {"id":24,"title":"Intel Core i9-13900K","brand":"Intel","category":"CPU","socket":"LGA1700","price":4299,"rating":4.9,"stock":4,"specs":{"cores":"24核32线程","baseClock":"3.0GHz","tdp":"125W","process":"Intel 7","gen":"13th"}},
    {"id":25,"title":"Intel Core i5-14600K","brand":"Intel","category":"CPU","socket":"LGA1700","price":1799,"rating":4.7,"stock":15,"specs":{"cores":"14核20线程","baseClock":"3.5GHz","tdp":"125W","process":"Intel 7","gen":"14th"}},
    {"id":26,"title":"Intel Core i7-14700K","brand":"Intel","category":"CPU","socket":"LGA1700","price":2899,"rating":4.8,"stock":8,"specs":{"cores":"20核28线程","baseClock":"3.4GHz","tdp":"125W","process":"Intel 7","gen":"14th"}},
    {"id":27,"title":"Intel Core i9-14900K","brand":"Intel","category":"CPU","socket":"LGA1700","price":4799,"rating":4.8,"stock":3,"specs":{"cores":"24核32线程","baseClock":"3.2GHz","tdp":"125W","process":"Intel 7","gen":"14th"}},
    # AMD AM4 (Zen1-Zen3)
    {"id":28,"title":"AMD Ryzen 5 1600","brand":"AMD","category":"CPU","socket":"AM4","price":899,"rating":4.3,"stock":10,"specs":{"cores":"6核12线程","baseClock":"3.2GHz","tdp":"65W","process":"14nm","gen":"Zen1"}},
    {"id":29,"title":"AMD Ryzen 7 1700","brand":"AMD","category":"CPU","socket":"AM4","price":1399,"rating":4.4,"stock":6,"specs":{"cores":"8核16线程","baseClock":"3.0GHz","tdp":"65W","process":"14nm","gen":"Zen1"}},
    {"id":30,"title":"AMD Ryzen 5 2600","brand":"AMD","category":"CPU","socket":"AM4","price":999,"rating":4.5,"stock":12,"specs":{"cores":"6核12线程","baseClock":"3.4GHz","tdp":"65W","process":"12nm","gen":"Zen+"}},
    {"id":31,"title":"AMD Ryzen 7 2700","brand":"AMD","category":"CPU","socket":"AM4","price":1499,"rating":4.5,"stock":5,"specs":{"cores":"8核16线程","baseClock":"3.2GHz","tdp":"65W","process":"12nm","gen":"Zen+"}},
    {"id":32,"title":"AMD Ryzen 5 3600","brand":"AMD","category":"CPU","socket":"AM4","price":1199,"rating":4.6,"stock":15,"specs":{"cores":"6核12线程","baseClock":"3.6GHz","tdp":"65W","process":"7nm","gen":"Zen2"}},
    {"id":33,"title":"AMD Ryzen 7 3700X","brand":"AMD","category":"CPU","socket":"AM4","price":1899,"rating":4.7,"stock":8,"specs":{"cores":"8核16线程","baseClock":"3.6GHz","tdp":"65W","process":"7nm","gen":"Zen2"}},
    {"id":34,"title":"AMD Ryzen 5 5600","brand":"AMD","category":"CPU","socket":"AM4","price":1099,"rating":4.7,"stock":25,"specs":{"cores":"6核12线程","baseClock":"3.5GHz","tdp":"65W","process":"7nm","gen":"Zen3"}},
    {"id":35,"title":"AMD Ryzen 5 5600X","brand":"AMD","category":"CPU","socket":"AM4","price":1199,"rating":4.7,"stock":20,"specs":{"cores":"6核12线程","baseClock":"3.7GHz","tdp":"65W","process":"7nm","gen":"Zen3"}},
    {"id":36,"title":"AMD Ryzen 7 5800X","brand":"AMD","category":"CPU","socket":"AM4","price":2099,"rating":4.8,"stock":10,"specs":{"cores":"8核16线程","baseClock":"3.8GHz","tdp":"105W","process":"7nm","gen":"Zen3"}},
    {"id":37,"title":"AMD Ryzen 9 5900X","brand":"AMD","category":"CPU","socket":"AM4","price":3099,"rating":4.8,"stock":5,"specs":{"cores":"12核24线程","baseClock":"3.7GHz","tdp":"105W","process":"7nm","gen":"Zen3"}},
    # AMD AM5 (Zen4-Zen5)
    {"id":38,"title":"AMD Ryzen 5 7600","brand":"AMD","category":"CPU","socket":"AM5","price":1399,"rating":4.7,"stock":18,"specs":{"cores":"6核12线程","baseClock":"3.8GHz","tdp":"65W","process":"5nm","gen":"Zen4"}},
    {"id":39,"title":"AMD Ryzen 7 7800X3D","brand":"AMD","category":"CPU","socket":"AM5","price":2599,"rating":4.9,"stock":12,"specs":{"cores":"8核16线程","baseClock":"4.2GHz","tdp":"120W","process":"5nm","gen":"Zen4"}},
    {"id":40,"title":"AMD Ryzen 9 7950X","brand":"AMD","category":"CPU","socket":"AM5","price":4499,"rating":4.9,"stock":4,"specs":{"cores":"16核32线程","baseClock":"4.5GHz","tdp":"170W","process":"5nm","gen":"Zen4"}},

    # ==================== 主板 (19款) ====================
    # LGA1151
    {"id":41,"title":"华硕 PRIME B250M-PLUS","brand":"华硕","category":"主板","socket":"LGA1151","price":599,"rating":4.3,"stock":8,"specs":{"chipset":"B250","formFactor":"M-ATX","memoryType":"DDR4","memorySlots":"2","maxMemory":"32GB","pcieSlots":"PCIe 3.0 x16"}},
    {"id":42,"title":"微星 H270 GAMING M3","brand":"微星","category":"主板","socket":"LGA1151","price":799,"rating":4.4,"stock":6,"specs":{"chipset":"H270","formFactor":"ATX","memoryType":"DDR4","memorySlots":"4","maxMemory":"64GB","pcieSlots":"PCIe 3.0 x16"}},
    # LGA1151-2
    {"id":43,"title":"华硕 TUF B360M-PLUS GAMING","brand":"华硕","category":"主板","socket":"LGA1151-2","price":699,"rating":4.5,"stock":10,"specs":{"chipset":"B360","formFactor":"M-ATX","memoryType":"DDR4","memorySlots":"2","maxMemory":"32GB","pcieSlots":"PCIe 3.0 x16"}},
    {"id":44,"title":"技嘉 B365M AORUS ELITE","brand":"技嘉","category":"主板","socket":"LGA1151-2","price":649,"rating":4.4,"stock":12,"specs":{"chipset":"B365","formFactor":"M-ATX","memoryType":"DDR4","memorySlots":"2","maxMemory":"64GB","pcieSlots":"PCIe 3.0 x16"}},
    {"id":45,"title":"微星 Z390-A PRO","brand":"微星","category":"主板","socket":"LGA1151-2","price":999,"rating":4.6,"stock":7,"specs":{"chipset":"Z390","formFactor":"ATX","memoryType":"DDR4","memorySlots":"4","maxMemory":"128GB","pcieSlots":"PCIe 3.0 x16"}},
    # LGA1200
    {"id":46,"title":"华硕 TUF GAMING B460M-PLUS","brand":"华硕","category":"主板","socket":"LGA1200","price":799,"rating":4.6,"stock":15,"specs":{"chipset":"B460","formFactor":"M-ATX","memoryType":"DDR4","memorySlots":"2","maxMemory":"128GB","pcieSlots":"PCIe 3.0 x16"}},
    {"id":47,"title":"技嘉 B560M AORUS ELITE","brand":"技嘉","category":"主板","socket":"LGA1200","price":749,"rating":4.5,"stock":14,"specs":{"chipset":"B560","formFactor":"M-ATX","memoryType":"DDR4","memorySlots":"2","maxMemory":"128GB","pcieSlots":"PCIe 4.0 x16"}},
    {"id":48,"title":"微星 MAG B560M BAZOOKA","brand":"微星","category":"主板","socket":"LGA1200","price":699,"rating":4.5,"stock":11,"specs":{"chipset":"B560","formFactor":"M-ATX","memoryType":"DDR4","memorySlots":"2","maxMemory":"128GB","pcieSlots":"PCIe 4.0 x16"}},
    # LGA1700
    {"id":49,"title":"华硕 TUF GAMING B660M-PLUS D4","brand":"华硕","category":"主板","socket":"LGA1700","price":899,"rating":4.6,"stock":20,"specs":{"chipset":"B660","formFactor":"M-ATX","memoryType":"DDR4","memorySlots":"2","maxMemory":"128GB","pcieSlots":"PCIe 4.0 x16"}},
    {"id":50,"title":"技嘉 B660M AORUS PRO DDR4","brand":"技嘉","category":"主板","socket":"LGA1700","price":849,"rating":4.5,"stock":18,"specs":{"chipset":"B660","formFactor":"M-ATX","memoryType":"DDR4","memorySlots":"2","maxMemory":"128GB","pcieSlots":"PCIe 4.0 x16"}},
    {"id":51,"title":"微星 PRO B660M-A DDR4","brand":"微星","category":"主板","socket":"LGA1700","price":799,"rating":4.5,"stock":16,"specs":{"chipset":"B660","formFactor":"M-ATX","memoryType":"DDR4","memorySlots":"4","maxMemory":"128GB","pcieSlots":"PCIe 4.0 x16"}},
    {"id":52,"title":"华硕 TUF GAMING B760M-PLUS WIFI","brand":"华硕","category":"主板","socket":"LGA1700","price":1099,"rating":4.7,"stock":22,"specs":{"chipset":"B760","formFactor":"M-ATX","memoryType":"DDR5","memorySlots":"2","maxMemory":"192GB","pcieSlots":"PCIe 4.0 x16"}},
    {"id":53,"title":"技嘉 B760M AORUS ELITE AX","brand":"技嘉","category":"主板","socket":"LGA1700","price":1049,"rating":4.6,"stock":19,"specs":{"chipset":"B760","formFactor":"M-ATX","memoryType":"DDR5","memorySlots":"2","maxMemory":"192GB","pcieSlots":"PCIe 4.0 x16"}},
    # AM4
    {"id":54,"title":"华硕 TUF GAMING B450M-PLUS","brand":"华硕","category":"主板","socket":"AM4","price":599,"rating":4.5,"stock":12,"specs":{"chipset":"B450","formFactor":"M-ATX","memoryType":"DDR4","memorySlots":"2","maxMemory":"64GB","pcieSlots":"PCIe 3.0 x16"}},
    {"id":55,"title":"微星 B450 TOMAHAWK","brand":"微星","category":"主板","socket":"AM4","price":699,"rating":4.6,"stock":10,"specs":{"chipset":"B450","formFactor":"ATX","memoryType":"DDR4","memorySlots":"4","maxMemory":"64GB","pcieSlots":"PCIe 3.0 x16"}},
    {"id":56,"title":"技嘉 B550M AORUS PRO-P","brand":"技嘉","category":"主板","socket":"AM4","price":749,"rating":4.6,"stock":14,"specs":{"chipset":"B550","formFactor":"M-ATX","memoryType":"DDR4","memorySlots":"2","maxMemory":"128GB","pcieSlots":"PCIe 4.0 x16"}},
    # AM5
    {"id":57,"title":"华硕 TUF GAMING B650M-PLUS WIFI","brand":"华硕","category":"主板","socket":"AM5","price":1299,"rating":4.7,"stock":16,"specs":{"chipset":"B650","formFactor":"M-ATX","memoryType":"DDR5","memorySlots":"2","maxMemory":"192GB","pcieSlots":"PCIe 5.0 x16"}},
    {"id":58,"title":"微星 MAG B650 TOMAHAWK WIFI","brand":"微星","category":"主板","socket":"AM5","price":1399,"rating":4.7,"stock":13,"specs":{"chipset":"B650","formFactor":"ATX","memoryType":"DDR5","memorySlots":"4","maxMemory":"192GB","pcieSlots":"PCIe 5.0 x16"}},
    {"id":59,"title":"技嘉 B650M AORUS ELITE AX","brand":"技嘉","category":"主板","socket":"AM5","price":1199,"rating":4.6,"stock":15,"specs":{"chipset":"B650","formFactor":"M-ATX","memoryType":"DDR5","memorySlots":"2","maxMemory":"192GB","pcieSlots":"PCIe 5.0 x16"}},

    # ==================== 显卡 (36款) ====================
    # NVIDIA GTX 9xx-10xx
    {"id":60,"title":"NVIDIA GeForce GTX 960","brand":"NVIDIA","category":"显卡","socket":"PCIe 3.0 x16","price":1299,"rating":4.0,"stock":3,"specs":{"gpuModel":"GTX 960","vram":"4GB GDDR5","length":"210mm","tdp":"120W","interface":"PCIe 3.0 x16"}},
    {"id":61,"title":"NVIDIA GeForce GTX 1060 6G","brand":"NVIDIA","category":"显卡","socket":"PCIe 3.0 x16","price":1599,"rating":4.3,"stock":8,"specs":{"gpuModel":"GTX 1060","vram":"6GB GDDR5","length":"250mm","tdp":"120W","interface":"PCIe 3.0 x16"}},
    {"id":62,"title":"NVIDIA GeForce GTX 1070","brand":"NVIDIA","category":"显卡","socket":"PCIe 3.0 x16","price":2499,"rating":4.4,"stock":5,"specs":{"gpuModel":"GTX 1070","vram":"8GB GDDR5","length":"267mm","tdp":"150W","interface":"PCIe 3.0 x16"}},
    {"id":63,"title":"NVIDIA GeForce GTX 1080 Ti","brand":"NVIDIA","category":"显卡","socket":"PCIe 3.0 x16","price":3999,"rating":4.6,"stock":3,"specs":{"gpuModel":"GTX 1080 Ti","vram":"11GB GDDR5X","length":"270mm","tdp":"250W","interface":"PCIe 3.0 x16"}},
    # NVIDIA GTX 16xx
    {"id":64,"title":"NVIDIA GeForce GTX 1650","brand":"NVIDIA","category":"显卡","socket":"PCIe 3.0 x16","price":1099,"rating":4.1,"stock":15,"specs":{"gpuModel":"GTX 1650","vram":"4GB GDDR6","length":"200mm","tdp":"75W","interface":"PCIe 3.0 x16"}},
    {"id":65,"title":"NVIDIA GeForce GTX 1660 SUPER","brand":"NVIDIA","category":"显卡","socket":"PCIe 3.0 x16","price":1499,"rating":4.4,"stock":12,"specs":{"gpuModel":"GTX 1660 SUPER","vram":"6GB GDDR6","length":"230mm","tdp":"125W","interface":"PCIe 3.0 x16"}},
    # NVIDIA RTX 20xx
    {"id":66,"title":"NVIDIA GeForce RTX 2060","brand":"NVIDIA","category":"显卡","socket":"PCIe 3.0 x16","price":2299,"rating":4.5,"stock":10,"specs":{"gpuModel":"RTX 2060","vram":"6GB GDDR6","length":"226mm","tdp":"160W","interface":"PCIe 3.0 x16"}},
    {"id":67,"title":"NVIDIA GeForce RTX 2070 SUPER","brand":"NVIDIA","category":"显卡","socket":"PCIe 3.0 x16","price":3299,"rating":4.6,"stock":6,"specs":{"gpuModel":"RTX 2070 SUPER","vram":"8GB GDDR6","length":"267mm","tdp":"215W","interface":"PCIe 3.0 x16"}},
    {"id":68,"title":"NVIDIA GeForce RTX 2080 Ti","brand":"NVIDIA","category":"显卡","socket":"PCIe 3.0 x16","price":5999,"rating":4.7,"stock":2,"specs":{"gpuModel":"RTX 2080 Ti","vram":"11GB GDDR6","length":"267mm","tdp":"250W","interface":"PCIe 3.0 x16"}},
    # NVIDIA RTX 30xx
    {"id":69,"title":"NVIDIA GeForce RTX 3060","brand":"NVIDIA","category":"显卡","socket":"PCIe 4.0 x16","price":2199,"rating":4.6,"stock":20,"specs":{"gpuModel":"RTX 3060","vram":"12GB GDDR6","length":"242mm","tdp":"170W","interface":"PCIe 4.0 x16"}},
    {"id":70,"title":"NVIDIA GeForce RTX 3060 Ti","brand":"NVIDIA","category":"显卡","socket":"PCIe 4.0 x16","price":2799,"rating":4.7,"stock":15,"specs":{"gpuModel":"RTX 3060 Ti","vram":"8GB GDDR6","length":"242mm","tdp":"200W","interface":"PCIe 4.0 x16"}},
    {"id":71,"title":"NVIDIA GeForce RTX 3070","brand":"NVIDIA","category":"显卡","socket":"PCIe 4.0 x16","price":3499,"rating":4.7,"stock":10,"specs":{"gpuModel":"RTX 3070","vram":"8GB GDDR6","length":"242mm","tdp":"220W","interface":"PCIe 4.0 x16"}},
    {"id":72,"title":"NVIDIA GeForce RTX 3080","brand":"NVIDIA","category":"显卡","socket":"PCIe 4.0 x16","price":4999,"rating":4.8,"stock":6,"specs":{"gpuModel":"RTX 3080","vram":"10GB GDDR6X","length":"285mm","tdp":"320W","interface":"PCIe 4.0 x16"}},
    {"id":73,"title":"NVIDIA GeForce RTX 3090","brand":"NVIDIA","category":"显卡","socket":"PCIe 4.0 x16","price":8999,"rating":4.9,"stock":3,"specs":{"gpuModel":"RTX 3090","vram":"24GB GDDR6X","length":"313mm","tdp":"350W","interface":"PCIe 4.0 x16"}},
    # NVIDIA RTX 40xx
    {"id":74,"title":"NVIDIA GeForce RTX 4060","brand":"NVIDIA","category":"显卡","socket":"PCIe 4.0 x16","price":2499,"rating":4.6,"stock":25,"specs":{"gpuModel":"RTX 4060","vram":"8GB GDDR6","length":"240mm","tdp":"115W","interface":"PCIe 4.0 x16"}},
    {"id":75,"title":"NVIDIA GeForce RTX 4060 Ti","brand":"NVIDIA","category":"显卡","socket":"PCIe 4.0 x16","price":3199,"rating":4.7,"stock":18,"specs":{"gpuModel":"RTX 4060 Ti","vram":"8GB GDDR6","length":"267mm","tdp":"160W","interface":"PCIe 4.0 x16"}},
    {"id":76,"title":"NVIDIA GeForce RTX 4070","brand":"NVIDIA","category":"显卡","socket":"PCIe 4.0 x16","price":4299,"rating":4.7,"stock":12,"specs":{"gpuModel":"RTX 4070","vram":"12GB GDDR6X","length":"261mm","tdp":"200W","interface":"PCIe 4.0 x16"}},
    {"id":77,"title":"NVIDIA GeForce RTX 4070 Ti SUPER","brand":"NVIDIA","category":"显卡","socket":"PCIe 4.0 x16","price":5999,"rating":4.8,"stock":8,"specs":{"gpuModel":"RTX 4070 Ti SUPER","vram":"16GB GDDR6X","length":"310mm","tdp":"285W","interface":"PCIe 4.0 x16"}},
    {"id":78,"title":"NVIDIA GeForce RTX 4080 SUPER","brand":"NVIDIA","category":"显卡","socket":"PCIe 4.0 x16","price":7999,"rating":4.8,"stock":5,"specs":{"gpuModel":"RTX 4080 SUPER","vram":"16GB GDDR6X","length":"336mm","tdp":"320W","interface":"PCIe 4.0 x16"}},
    {"id":79,"title":"NVIDIA GeForce RTX 4090","brand":"NVIDIA","category":"显卡","socket":"PCIe 4.0 x16","price":12999,"rating":4.9,"stock":2,"specs":{"gpuModel":"RTX 4090","vram":"24GB GDDR6X","length":"336mm","tdp":"450W","interface":"PCIe 4.0 x16"}},
    # NVIDIA RTX 50xx
    {"id":80,"title":"NVIDIA GeForce RTX 5070","brand":"NVIDIA","category":"显卡","socket":"PCIe 5.0 x16","price":4599,"rating":4.8,"stock":10,"specs":{"gpuModel":"RTX 5070","vram":"12GB GDDR7","length":"267mm","tdp":"250W","interface":"PCIe 5.0 x16"}},
    {"id":81,"title":"NVIDIA GeForce RTX 5080","brand":"NVIDIA","category":"显卡","socket":"PCIe 5.0 x16","price":8499,"rating":4.9,"stock":4,"specs":{"gpuModel":"RTX 5080","vram":"16GB GDDR7","length":"304mm","tdp":"360W","interface":"PCIe 5.0 x16"}},
    {"id":82,"title":"NVIDIA GeForce RTX 5090","brand":"NVIDIA","category":"显卡","socket":"PCIe 5.0 x16","price":16499,"rating":4.9,"stock":1,"specs":{"gpuModel":"RTX 5090","vram":"32GB GDDR7","length":"336mm","tdp":"575W","interface":"PCIe 5.0 x16"}},
    # AMD RX 5xx-6xxx
    {"id":83,"title":"AMD Radeon RX 580","brand":"AMD","category":"显卡","socket":"PCIe 3.0 x16","price":999,"rating":4.1,"stock":6,"specs":{"gpuModel":"RX 580","vram":"8GB GDDR5","length":"267mm","tdp":"185W","interface":"PCIe 3.0 x16"}},
    {"id":84,"title":"AMD Radeon RX 5700 XT","brand":"AMD","category":"显卡","socket":"PCIe 4.0 x16","price":2599,"rating":4.4,"stock":4,"specs":{"gpuModel":"RX 5700 XT","vram":"8GB GDDR6","length":"267mm","tdp":"225W","interface":"PCIe 4.0 x16"}},
    {"id":85,"title":"AMD Radeon RX 6600","brand":"AMD","category":"显卡","socket":"PCIe 4.0 x16","price":1699,"rating":4.5,"stock":14,"specs":{"gpuModel":"RX 6600","vram":"8GB GDDR6","length":"190mm","tdp":"132W","interface":"PCIe 4.0 x16"}},
    {"id":86,"title":"AMD Radeon RX 6600 XT","brand":"AMD","category":"显卡","socket":"PCIe 4.0 x16","price":2099,"rating":4.5,"stock":10,"specs":{"gpuModel":"RX 6600 XT","vram":"8GB GDDR6","length":"221mm","tdp":"160W","interface":"PCIe 4.0 x16"}},
    {"id":87,"title":"AMD Radeon RX 6700 XT","brand":"AMD","category":"显卡","socket":"PCIe 4.0 x16","price":2799,"rating":4.6,"stock":8,"specs":{"gpuModel":"RX 6700 XT","vram":"12GB GDDR6","length":"267mm","tdp":"230W","interface":"PCIe 4.0 x16"}},
    {"id":88,"title":"AMD Radeon RX 6800 XT","brand":"AMD","category":"显卡","socket":"PCIe 4.0 x16","price":4199,"rating":4.7,"stock":5,"specs":{"gpuModel":"RX 6800 XT","vram":"16GB GDDR6","length":"267mm","tdp":"300W","interface":"PCIe 4.0 x16"}},
    {"id":89,"title":"AMD Radeon RX 6900 XT","brand":"AMD","category":"显卡","socket":"PCIe 4.0 x16","price":5499,"rating":4.7,"stock":3,"specs":{"gpuModel":"RX 6900 XT","vram":"16GB GDDR6","length":"267mm","tdp":"300W","interface":"PCIe 4.0 x16"}},
    # AMD RX 7xxx
    {"id":90,"title":"AMD Radeon RX 7600","brand":"AMD","category":"显卡","socket":"PCIe 4.0 x16","price":2099,"rating":4.5,"stock":16,"specs":{"gpuModel":"RX 7600","vram":"8GB GDDR6","length":"204mm","tdp":"165W","interface":"PCIe 4.0 x16"}},
    {"id":91,"title":"AMD Radeon RX 7700 XT","brand":"AMD","category":"显卡","socket":"PCIe 4.0 x16","price":3199,"rating":4.6,"stock":10,"specs":{"gpuModel":"RX 7700 XT","vram":"12GB GDDR6","length":"267mm","tdp":"245W","interface":"PCIe 4.0 x16"}},
    {"id":92,"title":"AMD Radeon RX 7800 XT","brand":"AMD","category":"显卡","socket":"PCIe 4.0 x16","price":3699,"rating":4.7,"stock":8,"specs":{"gpuModel":"RX 7800 XT","vram":"16GB GDDR6","length":"267mm","tdp":"263W","interface":"PCIe 4.0 x16"}},
    {"id":93,"title":"AMD Radeon RX 7900 XT","brand":"AMD","category":"显卡","socket":"PCIe 4.0 x16","price":5399,"rating":4.8,"stock":4,"specs":{"gpuModel":"RX 7900 XT","vram":"20GB GDDR6","length":"287mm","tdp":"315W","interface":"PCIe 4.0 x16"}},
    {"id":94,"title":"AMD Radeon RX 7900 XTX","brand":"AMD","category":"显卡","socket":"PCIe 4.0 x16","price":6999,"rating":4.8,"stock":3,"specs":{"gpuModel":"RX 7900 XTX","vram":"24GB GDDR6","length":"287mm","tdp":"355W","interface":"PCIe 4.0 x16"}},
    # Intel Arc
    {"id":95,"title":"Intel Arc A770","brand":"Intel","category":"显卡","socket":"PCIe 4.0 x16","price":1899,"rating":4.2,"stock":8,"specs":{"gpuModel":"Arc A770","vram":"16GB GDDR6","length":"267mm","tdp":"225W","interface":"PCIe 4.0 x16"}},

    # ==================== 内存 (13款) ====================
    {"id":96,"title":"金士顿 DDR4 2666 8GB","brand":"金士顿","category":"内存","socket":"DDR4","price":149,"rating":4.2,"stock":50,"specs":{"type":"DDR4","speed":"2666MHz","capacity":"8GB","casLatency":"CL19","voltage":"1.2V"}},
    {"id":97,"title":"金士顿 DDR4 3200 8GB","brand":"金士顿","category":"内存","socket":"DDR4","price":179,"rating":4.3,"stock":45,"specs":{"type":"DDR4","speed":"3200MHz","capacity":"8GB","casLatency":"CL16","voltage":"1.2V"}},
    {"id":98,"title":"金士顿 DDR4 3200 16GB","brand":"金士顿","category":"内存","socket":"DDR4","price":329,"rating":4.4,"stock":40,"specs":{"type":"DDR4","speed":"3200MHz","capacity":"16GB","casLatency":"CL16","voltage":"1.2V"}},
    {"id":99,"title":"海盗船 DDR4 3600 16GB","brand":"海盗船","category":"内存","socket":"DDR4","price":399,"rating":4.5,"stock":35,"specs":{"type":"DDR4","speed":"3600MHz","capacity":"16GB","casLatency":"CL18","voltage":"1.35V"}},
    {"id":100,"title":"海盗船 DDR4 3600 32GB","brand":"海盗船","category":"内存","socket":"DDR4","price":699,"rating":4.5,"stock":20,"specs":{"type":"DDR4","speed":"3600MHz","capacity":"32GB","casLatency":"CL18","voltage":"1.35V"}},
    {"id":101,"title":"芝奇 DDR4 3600 16GB","brand":"芝奇","category":"内存","socket":"DDR4","price":429,"rating":4.6,"stock":30,"specs":{"type":"DDR4","speed":"3600MHz","capacity":"16GB","casLatency":"CL16","voltage":"1.35V"}},
    {"id":102,"title":"金士顿 DDR5 5600 16GB","brand":"金士顿","category":"内存","socket":"DDR5","price":399,"rating":4.4,"stock":35,"specs":{"type":"DDR5","speed":"5600MHz","capacity":"16GB","casLatency":"CL36","voltage":"1.25V"}},
    {"id":103,"title":"海盗船 DDR5 6000 16GB","brand":"海盗船","category":"内存","socket":"DDR5","price":449,"rating":4.5,"stock":30,"specs":{"type":"DDR5","speed":"6000MHz","capacity":"16GB","casLatency":"CL30","voltage":"1.35V"}},
    {"id":104,"title":"芝奇 DDR5 6000 16GB","brand":"芝奇","category":"内存","socket":"DDR5","price":499,"rating":4.6,"stock":28,"specs":{"type":"DDR5","speed":"6000MHz","capacity":"16GB","casLatency":"CL30","voltage":"1.35V"}},
    {"id":105,"title":"金士顿 DDR5 6400 32GB","brand":"金士顿","category":"内存","socket":"DDR5","price":899,"rating":4.6,"stock":18,"specs":{"type":"DDR5","speed":"6400MHz","capacity":"32GB","casLatency":"CL32","voltage":"1.4V"}},
    {"id":106,"title":"海盗船 DDR5 6800 32GB","brand":"海盗船","category":"内存","socket":"DDR5","price":1099,"rating":4.7,"stock":12,"specs":{"type":"DDR5","speed":"6800MHz","capacity":"32GB","casLatency":"CL34","voltage":"1.4V"}},
    {"id":107,"title":"芝奇 DDR5 7200 16GB","brand":"芝奇","category":"内存","socket":"DDR5","price":699,"rating":4.7,"stock":15,"specs":{"type":"DDR5","speed":"7200MHz","capacity":"16GB","casLatency":"CL34","voltage":"1.45V"}},
    {"id":108,"title":"海盗船 DDR5 7200 32GB","brand":"海盗船","category":"内存","socket":"DDR5","price":1399,"rating":4.8,"stock":8,"specs":{"type":"DDR5","speed":"7200MHz","capacity":"32GB","casLatency":"CL34","voltage":"1.45V"}},

    # ==================== NVMe (14款) ====================
    {"id":109,"title":"三星 970 EVO Plus 500GB","brand":"三星","category":"NVMe","socket":"M.2 NVMe","price":399,"rating":4.5,"stock":25,"specs":{"interface":"PCIe 3.0 x4","formFactor":"M.2 2280","capacity":"500GB","readSpeed":"3500MB/s","writeSpeed":"3300MB/s"}},
    {"id":110,"title":"三星 970 EVO Plus 1TB","brand":"三星","category":"NVMe","socket":"M.2 NVMe","price":599,"rating":4.6,"stock":30,"specs":{"interface":"PCIe 3.0 x4","formFactor":"M.2 2280","capacity":"1TB","readSpeed":"3500MB/s","writeSpeed":"3300MB/s"}},
    {"id":111,"title":"西部数据 SN750 1TB","brand":"西部数据","category":"NVMe","socket":"M.2 NVMe","price":549,"rating":4.5,"stock":22,"specs":{"interface":"PCIe 3.0 x4","formFactor":"M.2 2280","capacity":"1TB","readSpeed":"3470MB/s","writeSpeed":"3000MB/s"}},
    {"id":112,"title":"三星 980 PRO 1TB","brand":"三星","category":"NVMe","socket":"M.2 NVMe","price":799,"rating":4.7,"stock":20,"specs":{"interface":"PCIe 4.0 x4","formFactor":"M.2 2280","capacity":"1TB","readSpeed":"7000MB/s","writeSpeed":"5000MB/s"}},
    {"id":113,"title":"三星 980 PRO 2TB","brand":"三星","category":"NVMe","socket":"M.2 NVMe","price":1399,"rating":4.7,"stock":12,"specs":{"interface":"PCIe 4.0 x4","formFactor":"M.2 2280","capacity":"2TB","readSpeed":"7000MB/s","writeSpeed":"5000MB/s"}},
    {"id":114,"title":"西部数据 SN850X 1TB","brand":"西部数据","category":"NVMe","socket":"M.2 NVMe","price":749,"rating":4.7,"stock":18,"specs":{"interface":"PCIe 4.0 x4","formFactor":"M.2 2280","capacity":"1TB","readSpeed":"7300MB/s","writeSpeed":"6300MB/s"}},
    {"id":115,"title":"西部数据 SN850X 2TB","brand":"西部数据","category":"NVMe","socket":"M.2 NVMe","price":1299,"rating":4.7,"stock":10,"specs":{"interface":"PCIe 4.0 x4","formFactor":"M.2 2280","capacity":"2TB","readSpeed":"7300MB/s","writeSpeed":"6600MB/s"}},
    {"id":116,"title":"致态 TiPlus7100 1TB","brand":"致态","category":"NVMe","socket":"M.2 NVMe","price":499,"rating":4.6,"stock":25,"specs":{"interface":"PCIe 4.0 x4","formFactor":"M.2 2280","capacity":"1TB","readSpeed":"7000MB/s","writeSpeed":"6000MB/s"}},
    {"id":117,"title":"致态 TiPlus7100 2TB","brand":"致态","category":"NVMe","socket":"M.2 NVMe","price":899,"rating":4.6,"stock":15,"specs":{"interface":"PCIe 4.0 x4","formFactor":"M.2 2280","capacity":"2TB","readSpeed":"7000MB/s","writeSpeed":"6000MB/s"}},
    {"id":118,"title":"三星 990 PRO 1TB","brand":"三星","category":"NVMe","socket":"M.2 NVMe","price":899,"rating":4.8,"stock":16,"specs":{"interface":"PCIe 4.0 x4","formFactor":"M.2 2280","capacity":"1TB","readSpeed":"7450MB/s","writeSpeed":"6900MB/s"}},
    {"id":119,"title":"三星 990 PRO 2TB","brand":"三星","category":"NVMe","socket":"M.2 NVMe","price":1599,"rating":4.8,"stock":8,"specs":{"interface":"PCIe 4.0 x4","formFactor":"M.2 2280","capacity":"2TB","readSpeed":"7450MB/s","writeSpeed":"6900MB/s"}},
    {"id":120,"title":"英睿达 T700 1TB","brand":"英睿达","category":"NVMe","socket":"M.2 NVMe","price":1099,"rating":4.7,"stock":10,"specs":{"interface":"PCIe 5.0 x4","formFactor":"M.2 2280","capacity":"1TB","readSpeed":"9400MB/s","writeSpeed":"8500MB/s"}},
    {"id":121,"title":"英睿达 T700 2TB","brand":"英睿达","category":"NVMe","socket":"M.2 NVMe","price":1899,"rating":4.7,"stock":6,"specs":{"interface":"PCIe 5.0 x4","formFactor":"M.2 2280","capacity":"2TB","readSpeed":"9400MB/s","writeSpeed":"9500MB/s"}},
    {"id":122,"title":"三星 990 EVO 1TB","brand":"三星","category":"NVMe","socket":"M.2 NVMe","price":599,"rating":4.6,"stock":20,"specs":{"interface":"PCIe 4.0 x4","formFactor":"M.2 2280","capacity":"1TB","readSpeed":"5000MB/s","writeSpeed":"4200MB/s"}},

    # ==================== 机箱 (11款) ====================
    {"id":123,"title":"酷冷至尊 MasterBox Q300L","brand":"酷冷至尊","category":"机箱","socket":"ATX","price":259,"rating":4.2,"stock":20,"specs":{"formFactor":"M-ATX","maxGpuLength":"360mm","radiatorSupport":"240mm","driveBays":"2x 2.5\"","fans":"1x 120mm"}},
    {"id":124,"title":"先马 平头哥M1","brand":"先马","category":"机箱","socket":"ATX","price":199,"rating":4.1,"stock":30,"specs":{"formFactor":"M-ATX","maxGpuLength":"350mm","radiatorSupport":"240mm","driveBays":"2x 2.5\" + 2x 3.5\"","fans":"2x 120mm"}},
    {"id":125,"title":"乔思伯 D31","brand":"乔思伯","category":"机箱","socket":"ATX","price":399,"rating":4.5,"stock":15,"specs":{"formFactor":"M-ATX","maxGpuLength":"365mm","radiatorSupport":"360mm","driveBays":"2x 2.5\" + 2x 3.5\"","fans":"3x 120mm"}},
    {"id":126,"title":"联力 216","brand":"联力","category":"机箱","socket":"ATX","price":599,"rating":4.6,"stock":12,"specs":{"formFactor":"ATX","maxGpuLength":"392mm","radiatorSupport":"360mm","driveBays":"4x 2.5\" + 2x 3.5\"","fans":"2x 160mm"}},
    {"id":127,"title":"追风者 G360A","brand":"追风者","category":"机箱","socket":"ATX","price":499,"rating":4.5,"stock":14,"specs":{"formFactor":"ATX","maxGpuLength":"380mm","radiatorSupport":"360mm","driveBays":"2x 2.5\" + 2x 3.5\"","fans":"3x 120mm"}},
    {"id":128,"title":"NZXT H7 Flow","brand":"NZXT","category":"机箱","socket":"ATX","price":699,"rating":4.6,"stock":10,"specs":{"formFactor":"ATX","maxGpuLength":"400mm","radiatorSupport":"360mm","driveBays":"2x 2.5\" + 2x 3.5\"","fans":"2x 140mm"}},
    {"id":129,"title":"海盗船 4000D Airflow","brand":"海盗船","category":"机箱","socket":"ATX","price":799,"rating":4.7,"stock":8,"specs":{"formFactor":"ATX","maxGpuLength":"360mm","radiatorSupport":"360mm","driveBays":"2x 2.5\" + 2x 3.5\"","fans":"2x 120mm"}},
    {"id":130,"title":"酷冷至尊 H500M","brand":"酷冷至尊","category":"机箱","socket":"ATX","price":1299,"rating":4.7,"stock":5,"specs":{"formFactor":"ATX","maxGpuLength":"412mm","radiatorSupport":"360mm","driveBays":"2x 2.5\" + 2x 3.5\"","fans":"2x 200mm"}},
    {"id":131,"title":"联力 O11 Dynamic EVO","brand":"联力","category":"机箱","socket":"ATX","price":999,"rating":4.8,"stock":7,"specs":{"formFactor":"ATX","maxGpuLength":"420mm","radiatorSupport":"360mm","driveBays":"4x 2.5\" + 2x 3.5\"","fans":"3x 120mm"}},
    {"id":132,"title":"追风者 NV7","brand":"追风者","category":"机箱","socket":"ATX","price":899,"rating":4.7,"stock":6,"specs":{"formFactor":"ATX","maxGpuLength":"435mm","radiatorSupport":"360mm","driveBays":"4x 2.5\" + 4x 3.5\"","fans":"2x 140mm"}},
    {"id":133,"title":"Fractal Design Torrent","brand":"Fractal","category":"机箱","socket":"ATX","price":1499,"rating":4.8,"stock":4,"specs":{"formFactor":"ATX","maxGpuLength":"461mm","radiatorSupport":"360mm","driveBays":"4x 2.5\" + 6x 3.5\"","fans":"2x 180mm + 3x 140mm"}},
]
