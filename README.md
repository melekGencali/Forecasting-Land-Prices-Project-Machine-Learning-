# FORECASTING LAND PRICES PROJECT 

---
![arsa](https://cdn-images-1.medium.com/max/600/1*xnq7QjVHQELbWcpEPn_IaQ.jpeg)

Web Scraping -Regression İle Satılık Arsa Fiyatı Tahminlemesi
Merhabalar, bu proje Scrapy, Data Proprocessing ve ML algoritmaları hakkında bilgi vermek amacıyla yapılmıştır. Bu sebeple tahmin çok iyi bir sonuç değilir. ilk olarak Scrapy ile Web Scraping işlemi yapılmıştır.  Bu linkten Scrapy hakkında bilgi edinebilirsiniz. Sonrasında tahminleme işlemine geçilmiştir. Projemizi adım adım anlatacağız. Proje kodlarına sayfa sonunda verilen linkten ulaşabilirsiniz. 


---

## - Web Scraping
Web crawl işlemi için genellikle Scrapy ya da BeautifulsSoup kullanılır. Biz Scrapy paketini kullandık. İlk olarak veri çekeceğimiz site açılır. Sayfa üzerinde sağ tıklanarak incele denilir.

![img](https://cdn-images-1.medium.com/max/800/1*Dd1ywfXBMzbUmnpznn0J5A.png)

İstenilen kısım liste içerisindeki linklerdir. Bu linkler üzerinden ilan içeriğine gidilir. Şu adımları izleyerek Scrapy projesi oluşturup veri çekme işlemini halledeceğiz.

- PyCharm üzerinde python projesi oluşturuldu.
- PyCharm' da terminal üzerinde: 

  1. scrapy startproject 'projeName' 
  2. cd 'projeName' 
  3. scrapy genspider 'spiderName' 'web sitesi url' girilir.
   
- Scrapy projesi oluşturulduktan sonra sağ üst köşedeki ' Edit Run/Debug configurations' kutucuk açılıp parameters alanına ' crawl proje -o veri.json' yazılır.
- Proje çalıştırılır ve veriler json formatında dosyaya kaydedilir.

![crawl](https://cdn-images-1.medium.com/max/800/1*uxqOStIDImfiPBIt_2oTrw.png)

Web Scraping işlemi için proje kodlarının bir kısmı verilmiştir.Ekran çıktımız şu şekildedir:

![çıktı](https://cdn-images-1.medium.com/max/800/1*egXUIGmASnzW5zj4s8cN1g.png)

Artık Machine Learning regression algoritmaları ile tahminleme işlemine başlayabilirizz!


---

##  -Regression ile Machine Learning
Veri setimizin pandas, matplotlib gibi kütüphaneler ile görsel olarak incelenmesi için projede jupyter notebook kullanılacaktır. İlk olarak projede Jupyter Notebook create edeceğiz ve gerekli kütüphaneleri (jupyter, pandas, numpy …) import edeceğiz. Web sitesinden çektiğimiz veriler json formatındadır. Csv ya da xlsx formatına çevrilerek pandas ile okuma işlemi tercih edilir. Burada yapacağımız işlemler sırasıyla şu şekildedir:

 1. Verisetini düzenleme (web sitesinden çekilen veriler büyük küçük harf yada farklı formatlarda gelebilir.)
 2. Tahminleme işlemi için önemli kategorik değişkenler olabilir. Bunları modelde kullanmak istediğimiz zaman sayısal değerlere (1, 0) dönüştürmemiz gerekir ve bunun için için LabelEncoder kullandık. Burada dönüşüm yaptığımızda float bir sonuç için kategorik olan yani 1 veya 0 gibi integer değerleri 1 ile 0 arasında değerlere atar. Bu şekilde yapısal bozukluk olacaktır. Bunu çözmek için One Hot dönüşümü ile Dummy Değişken Tuzağı yöntemi kullanılacaktır.

 ![one_hot](https://cdn-images-1.medium.com/max/800/1*4L-pL5-oN2sy4_hDuCPqug.png)

 3. Eksik değerler gerekli algoritmalar ile doldurulacaktır. Öncelikle eksik değerleri missingno ve heatmap gibi algoritmalarla gözlemleyelim.
 
 ![missing](https://cdn-images-1.medium.com/max/800/1*yzjb7bH7yoYla_pv-xRzRg.png)
 ![missing2](https://cdn-images-1.medium.com/max/800/1*J07AzHhsUqhoGQ9_XZx6Og.png)
 
- Not: ada içerisinde parsel barındırır. Bu sebeple aralarında ilişki olduğundan birlikte korelasyona sokulmamalıdır. Sonuç yanlış verir. Ada kolonunu kaldırdık.
```df_train = df_train.drop(["ADA"], axis = 1) ```

- Kategorik değişkenlerde eksik değer olduğunda önce ilgili algoritmalar ile eksik değerler doldurulur. Sonra one hot dönüşümü yapılır:
```df_train["TAPU_DURUMU"].fillna(df_train["TAPU_DURUMU"].mode()[0],inplace=True)```

- Kategorik değişkenler için Mod alma işlemi, numeric değişkenler için Mean ve Median alma işlemleri ile eksik değerler dolduruldu. 
Not: Bazı değişkenler birbiriyle ilişkili olduğundan eksik alanlar doldurulurken gruplama işlemi ile dolduruldu:

```df_train["METREKARE_BIRIM_FIYAT"].fillna(df_train.groupby("METREKARE")["METREKARE_BIRIM_FIYAT"].transform("mean"),inplace=True)```

 4. Artık veriler temizlenecektir. (Örneğin fiyat değişkeni için 1.000 ile 100.000.000.000 arasında değerler olduğunu düşünelim. Burada 1.000 fiyatına sahip 5 tane arsa var ve elimizde 14.957 arsa verisi var. Burada 1.000 fiyatındaki arsa,  tahmin sonucunu kötü yönde etkileyeceğinden bu 5 arsa verisini veri setimizden sileriz.) Artık verileri görselleştirmek için boxplot kullanılacaktır.

![boxplot](https://cdn-images-1.medium.com/max/800/1*Om_N3e5438HLmkKTBgquAw.png)

Burada 40.000 sonrası için veriler azalmaya başlıyor. 2.000 ve öncesi için veriler incelendiğinde yine azalma görülmektedir. Bu sebeple :



```
df_train = df_train.loc[(df_train["FIYAT"] < 4300000) & (df_train["FIYAT"] > 2000)] 
df_train.reset_index()
```

Metrekare, Parsel içinde artık veri temizleme işlemlerini yaptık. Ancak onlarda gözlemlenerek tahminen silme işlemi yerine gerekli formüllerle bu işlem yapılmıştır:
 
```
Q1=df_train["METREKARE"].quantile(0.25)
Q3=df_train["METREKARE"].quantile(0.75)
IQR=Q3-Q1
alt_sinir=Q1–1.5*IQR
ust_sinir=Q3+1.5*IQR 
df_train = df_train.loc[(df_train["METREKARE"] < ust_sinir) & (df_train["METREKARE"] > alt_sinir)]
df_train.reset_index()
```

5. Correlation Matrix For işlemi yapıldı. ( Değişkenlerin birbiriyle olan ilişkisine bakılır. -1 ile 1 arasında sonuç üretir. -1 e ne kadar yakın ise (-0.58, 0.1 , 0.3, vb.) o kadar ilişkisiz, 1 e ne kadar yakın ise o kadar (0.6, 0.9, 1.0 vb.) ilişkilidir. Burada One Hot dönüşümü ile kategorik değişkenleri numeric değerlere çevirdiğimizden kolon sayısı artmıştır.

![corr](https://cdn-images-1.medium.com/max/800/1*e8-ZlWlCLyuv8TIVsyYSRQ.png)

6. Select Features aşaması yapılacaktır. Özellik seçimi için Extra Tree Classifier'ı kullanıldı.

![select_features](https://cdn-images-1.medium.com/max/800/1*erITdsz3fOQ_r7Zadoz_SQ.png)
![ExtraTreeClassifier](https://cdn-images-1.medium.com/max/800/1*1x8A6LooaWvqfqlVGsKwyw.png)
![ExtraTreeClassifier2](https://cdn-images-1.medium.com/max/800/1*vz75anaahsIAA5MLh4mo4w.png)
![ExtraTreeClassifier3](https://cdn-images-1.medium.com/max/800/1*uYhnC021ddkYgImhkoCY7A.png)

7. Model seçimi için seçilen değişkenlere OLS uyguladık. Burada en çok dikkat etmemiz gereken yerler "  R-squared (uncentered) ,Prob (F-statistic) ,std err,P>|t|, Cond. No. " 

![ols](https://cdn-images-1.medium.com/max/800/1*plIiYVqlh-K5LopKUPyG0w.png)
![ols2](https://cdn-images-1.medium.com/max/800/1*rgsT3PGkLWeeOB4kIV70zg.png)

- R-squared (uncentered): =Her bir noktanın ortalamaya uzaklığının karesine de Ortalamaya Uzaklığın Kareler Toplamı (OUKT) diyelim. Ortalamaya Uzaklığın Kareler Toplamı (OUKT) = TOPLAM(yi - ȳ)2 formülü ile gösterilir. R2 ise bu iki değerden faydalanılarak hesaplanır: R2 = 1 - (AKT/OUKT)
- Not: Artıkların toplamının ortalamaların toplamına olan oranı ne kadar küçük ise R2 o kadar yüksek olacaktır. R2'ın yüksek olması regresyon model uyumunun iyi olduğunu gösterir. Tüm noktalar regresyon doğrusu üzerinde olsaydı mükemmel bir modelimiz olurdu. Tüm noktalar doğru üzerinde olduğunda Artıkların Kareler Toplamı (AKT) sıfır olacağından R2'e de 1'e eşit olacak ve alabileceği en yüksek değeri alacaktır.

- Adj. R-squared (uncentered): Regresyon iyilik uyum indeksi (goodness of fit) olarak R2 kullandığımızda artıkların toplam karesi ne kadar düşük olursa uyum o kadar yüksek oluyor. Ancak bağımsız değişken sayısı arttıkça payda düşmeye devam edecektir. Böylelikle R2 düşmeyecek ve ne kadar çok değişken modele katılırsa o kadar yüksek bir uyum ortaya çıkacaktır. Model karmaşıklığını azaltmak ve anlaşılabilir, yorumlanabilir (interpretable) modeller oluşturmak için hedef değişkene etkisi olmayan, az olan, etkisi ihmal edilebilen değişkenler modele dahil edilmez ve kafalar bulandırılmaz. Bu sebeple iyilik uyum indeksi kullanırken R2 geliştirerek düzeltilmiş R2 kullanılmaktadır. Düzeltilmiş R2 'nin R2 'den farkı gereksiz eklenen bağımsız değişkenleri cezalandırıyor olmasıdır. 
- Prob (F-statistic): Prob (F) değeri, tüm model için boş hipotezin doğru olma olasılığıdır (yani, tüm regresyon katsayıları sıfırdır). Örneğin, Prob (F) 0.01000 değerine sahipse, tüm regresyon parametrelerinin sıfır olma ihtimali 100'de 1'dir. Bu düşük bir değer, regresyon parametrelerinin en azından bazılarının sıfır olmadığı ve regresyon denkleminin verileri uydurmada bir miktar geçerliliğe sahip olduğu anlamına gelir (yani, bağımsız değişkenler, bağımlı değişkene göre tamamen rastgele değildir).
- std err : bize, hesapladığımız ortalama değerin gerçek değerden ne derece sapacağını söyler. Yukarıdaki formülden de görebileceğimiz üzere n arttıkça SE düşecektir. Yani ne kadar çok örneklem üretirsek SE düşer, sapma azalır, dolayısıyla tahminimiz gerçek değere daha çok yaklaşır.
- P>|t|: Bir değişkenin p değeri, önem düzeyinizden düşükse , örnek verileriniz tüm popülasyon için boş hipotezi reddetmek için yeterli kanıt sağlar. Verileriniz , sıfır olmayan bir korelasyon olduğu hipotezini destekliyor . Bağımsız değişken istatistiksel olarak anlamlıdır ve muhtemelen regresyon modelinize değerli bir katkıdır.
 Öte yandan, anlamlılık düzeyinden daha büyük bir p değeri, numunenizde sıfır olmayan bir korelasyonun var olduğu sonucuna varmak için yeterli kanıt olmadığını gösterir. Değişkenlerin nihai modele dahil edilip edilmeyeceğine karar vermek için katsayı p değerlerinin kullanılması standart uygulamadır . İstatistiksel olarak önemli olmayan değişkenleri tutmak, modelin kesinliğini azaltabilir.
- Cond. No. : Koşul numarası, doğrusallığı teşhis etmeye yardımcı olmak için kullanılır. Eşdoğrusallık, bir bağımsız değişkenin diğer değişkenler kümesinin doğrusal bir kombinasyonu olmaya yakın olduğu zamandır. Düşük değer vermesi beklenir.

8. df.describe().T ile sayısal değişkenler kontrol edilir. 
Burada değişkenlerin dağılımları gözlemlenir. Çarpıklık durumu düzeltilir.

![Dağılım](https://cdn-images-1.medium.com/max/800/0*QqHIny3eUT9TBQOl.jpg)
Basit bir ifadeyle, çarpıklık, rastgele bir değişkenin olasılık dağılımının ne kadar sapma olduğunun ölçüsüdür.Normal dağılım, herhangi bir çarpıklık olmadan olasılık dağılımıdır. Temelde normal bir dağılım olan simetrik dağılımı gösteren aşağıdaki görüntüye bakabilir ve kesikli çizginin her iki tarafında simetrik olduğunu görebilirsiniz. Bunun dışında iki çeşit çarpıklık vardır: 

-Olumlu Eğrilik: dağılımın çarpıklığının sağda olmasıdır; ortalamanın medyandan daha büyük olmasına ve sonunda sağa doğru hareket etmesine neden olur. Ayrıca, mod medyanın sol tarafında bulunan dağılımın en yüksek frekansında gerçekleşir. Bu nedenle, mod <medyan <ortalama.
-Olumsuz Eğrilik : negatif eğimli bir dağılım, kuyruğun sol tarafındaki dağılımdır. Negatif çarpık dağılım için çarpıklık değeri sıfırdan küçüktür. ortalama <medyan <modu. 

df.describe().T ile çıkan tabloda mean ile %50 arasındaki fark ne kadar fazla ise o kadar çarpıklık durumu fazladır. Bu durumu çözmek için ' Power Dönüşümü', 'Log  Dönüşümü ' , 'Exponential Dönüşüm' yöntemleri kullanılır. Biz Log dönüşümü uygulayacağız. Örneğin: 

```df["FIYAT"] = np.log(df["FIYAT"])```

![dağılım2](https://cdn-images-1.medium.com/max/800/1*0MpsMW2CiiSuIskAHwwqYQ.png)

Log dönüşümü uygulandıktan sonra tablomuzu kontrol edelim.

![DağılımKontrol](https://cdn-images-1.medium.com/max/800/1*b9Xvr8-C_hV3vhiB-n3zCg.png)

9. Kullanabileceğimiz modelleri seçip test veri seti üzerinde score' ları inceledik. En yüksek olanlar seçilir.
![model](https://cdn-images-1.medium.com/max/800/1*pbT2AFpXORpOi01V53yfwQ.png)

10. Cross Validation işlemi ile uygulanan modeller için en yüksek score sonucu verenler seçilir.
![cv](https://cdn-images-1.medium.com/max/800/1*s3xVvMm5dtNMQRxy03NATQ.png)

11. MSE, MAE gibi algoritmalarla test veri setine uygulanan modellerin hata kontrolleri yapılır. En az hata veren algoritma önceki seçilen algoritmalar içinden seçilir ve o model veri setine uygulanır.
![MAE](https://cdn-images-1.medium.com/max/800/1*8uGFnr-A2Pg2gZcdEe_FLQ.png)

12. Sonuç kontrol edilir.
![sonuç](https://cdn-images-1.medium.com/max/800/1*D_lReH8QwVnh_kbk1uqhUQ.png)
![sonuç2](https://cdn-images-1.medium.com/max/800/1*V-dNl_lvpzhQ7Az0ygDr-Q.png)

13. Model kaydedilir.
![pickle](https://cdn-images-1.medium.com/max/800/1*yUJaIZ3RfWV_j8C2yYvViA.png)

Sonuç olarak, web sitesinden çekilen veri seti çok eksik ve artık değer barındırdığından güzel bir sonuç elde edemedik. Ancak Web Scraping ve veri biliminde kullanılan algoritmalar ile genel bir çalışma yaptık. Umarım beğenirsiniz. Bir sonraki projede görüşmek üzere !!!

Proje kodlarına buradan erişebilirsiniz : https://github.com/melekGencali/Forecasting-Land-Prices-Project-Machine-Learning-/tree/master
