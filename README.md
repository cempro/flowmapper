# FlowMapper 1.0.0

FlowMapper, düğüm koordinatları, isteğe bağlı düğüm adları ve kare bir akış (OD) matrisi kullanarak QGIS içinde akış çizgileri ve isteğe bağlı düğüm özet katmanı üretir. Aynı paket hem QGIS 2.x/Python 2.7/PyQt4 hem de QGIS 3.x/Python 3/PyQt5 üzerinde çalışacak biçimde yazılmıştır.

## Kurulum

### QGIS 3

1. `FlowMapper_QGIS2_QGIS3_v1.0.0.zip` dosyasını açmayın.
2. **Plugins > Manage and Install Plugins > Install from ZIP** menüsünü açın.
3. ZIP dosyasını seçip kurulumu tamamlayın.
4. Gerekirse **Installed** bölümünden FlowMapper'ı etkinleştirin.

### QGIS 2

QGIS 2 sürümünüzde ZIP'ten kurulum seçeneği varsa aynı ZIP'i kullanın. Yoksa ZIP içindeki `FlowMapper` klasörünü aşağıdaki eklenti klasörüne çıkarın ve QGIS'i yeniden başlatın:

- Windows: `%USERPROFILE%\\.qgis2\\python\\plugins\\`
- Linux: `~/.qgis2/python/plugins/`

Eklenti ek bir Python paketi istemez; QGIS ile birlikte gelen GDAL/OGR bağlarını kullanır.

## Girdi dosyaları

Girdi dosyaları UTF-8 düz metin olmalı; boş satırlar atlanır. Sayılarda ondalık ayırıcı olarak nokta (`.`) kullanın ve başlık satırı eklemeyin. Düğüm koordinatları ile akış matrisi zorunlu, düğüm adları isteğe bağlıdır.

### 1. Düğüm koordinatları

Her satırda boşlukla ayrılmış bir `X Y` çifti bulunur. EPSG:4326 için sıra `boylam enlem` olmalıdır.

```text
28.80 41.20
30.50 36.90
42.10 41.20
40.70 37.40
```

### 2. Düğüm adları (isteğe bağlı)

Dosya verilirse her düğüm için aynı sırada bir tam satır bulunur. Adların içinde boşluk olabilir. Dosya boş bırakılırsa kare matrisin satır/sütun sayısına göre `node1`, `node2`, ... `nodeN` adları otomatik üretilir.

```text
istanbul
antalya
artvin
mardin
```

### 3. Akış matrisi

`N` düğüm için matris tam olarak `N x N` olmalıdır. `i`. satırdaki `j`. değer, `i` düğümünden `j` düğümüne akıştır.

```text
0   270 10  5
200 0   40  15
120 130 0   20
70  60  25  0
```

## Akış türleri

- **Two-way:** Her yön için ayrı bir akış çizgisi oluşturur. `magnitude = M[i][j]`.
- **Gross:** Her düğüm çifti için iki yöndeki akışları birleştirir. `magnitude = M[i][j] + M[j][i]`.
- **Net:** Karşıt yönlerdeki akışların farkını, büyük akışın yönünde gösterir. `magnitude = |M[i][j] - M[j][i]|`.

**Flow lines** çıktı satırının altındaki geometri seçenekleri birbirini dışlar:

- **Generate straight flow lines:** Her akışı iki noktalı düz bir çizgi olarak üretir ve varsayılan seçenektir.
- **Generate curved flow lines:** Her akışı yumuşak, çok noktalı Bézier polyline olarak üretir. Karşıt Two-way akışları eğrinin farklı taraflarından geçer.

Varsayılan olarak sıfır büyüklüklü akışlar ve matrisin diyagonalindeki iç akışlar yazılmaz. **Include inner flows (diagonal, zero-length)** seçilirse diyagonal matris değerleri sıfır uzunluklu çizgiler olarak çıktıya eklenir.

**Add result to map** seçildiğinde QGIS, çizgilerin üzerine `magnitude` değerini yazar. Net oku çizginin/eğrinin merkezinde, Two-way oku son noktada gösterilir. Two-way çizgileri, karşıt yönlerin üst üste binmesini azaltmak için yönlerine göre hafifçe ötelenir. Gross çizgileri yönsüz gösterilir. **Create flow nodes** seçilmişse düğüm katmanı da haritaya eklenir. **Color nodes by flow gain/loss** seçeneği düğümleri Gain için yeşil, Loss için kırmızı ve Balanced için gri renklendirir.

## Çıktı alanları

### Flow lines

| Alan | İçerik |
| --- | --- |
| `flow_id` | Benzersiz çizgi numarası |
| `from_id`, `to_id` | 1'den başlayan kaynak/hedef düğüm numarası |
| `from_name`, `to_name` | Kaynak/hedef düğüm adı |
| `name_x1y1`, `name_x2y2` | Eski FlowMapper alan adlarıyla uyumlu kaynak/hedef adları |
| `magnitude` | Seçilen Two-way, Gross veya Net akış büyüklüğü |
| `mag_label` | Harita üzerinde kullanılan, gereksiz sıfırlar atılmış büyüklük etiketi |
| `forward`, `reverse` | Çizginin kaynak-hedef yönündeki ham değer ve ters yön değeri |
| `length_km` | Eğri seçiminden bağımsız doğrudan düğüm mesafesi; coğrafi CRS'de büyük daire, projeksiyonlu CRS'de düzlemsel uzunluk (km) |
| `coord_x1` ... `coord_y2` | Kaynak ve hedef koordinatları |
| `flow_type` | `two_way`, `gross` veya `net` |

Gross çizginin geometrik başlangıç yönü yalnızca kararlı kayıt düzeni içindir; Gross akış yönsüzdür. Two-way ve Net çizgilerinde geometrinin ilk noktası kaynağı, ikinci noktası hedefi gösterir.

### Flow nodes (isteğe bağlı)

**Create flow nodes** seçildiğinde **Flow nodes** çıktı yolu etkinleşir ve koordinat dosyasındaki her düğüm için bir point feature oluşturulur.

| Alan | İçerik |
| --- | --- |
| `node_id` | 1'den başlayan düğüm numarası |
| `node_name` | Dosyadan okunan veya otomatik oluşturulan düğüm adı |
| `forward` | Matris satır toplamı; düğümden çıkan toplam akış |
| `reverse` | Matris sütun toplamı; düğüme gelen toplam akış |
| `net` | İşaretli net değer: `forward - reverse` |
| `gain_loss` | `gain`, `loss` veya `balanced` sınıfı |
| `coord_x`, `coord_y` | Koordinat TXT dosyasından alınan düğüm koordinatları |

Pozitif `net` değeri net outgoing ve `loss`; negatif değer net incoming ve `gain`; sıfır değer ise `balanced` olarak sınıflandırılır. Diyagonal matris değerleri hem `forward` hem `reverse` toplamına girer ve `net` hesabında birbirini götürür.

## Bu sürümün kapsamı

- Zorunlu koordinat/matris ve isteğe bağlı ad girdilerinin ayrıntılı doğrulanması
- Two-way, Gross ve Net hesapları
- CRS/EPSG tanımı ve `length_km`
- UTF-8 veya otomatik üretilen düğüm adları
- Düz veya eğri akış çizgisi ve isteğe bağlı düğüm özeti Shapefile çıktıları
- Büyüklük etiketleri, yön okları, gain/loss düğüm renkleri ve sonuçları haritaya ekleme
- About penceresi
- QGIS 2 ve QGIS 3 ortak kod tabanı

Gelişmiş sınıflandırılmış semboloji ve filtreleme bu çekirdek sürüme dahil değildir.

## Atıf

Original FlowMapper concept and development: **Cem GULLUOGLU**  
Inspired by **Alan Glennon’s FlowpyGIS**

License: GNU GPL v2 or later.
