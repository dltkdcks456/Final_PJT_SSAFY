### ๐ 11.27(์ํ ์ ๊ณต ์คํธ๋ฆฌ๋ฐ ์ฌ์ดํธ ์ถ๊ฐ)

- OTT์ฌ์ดํธ๊ฐ ์๋ ์ํ ์ถ์ฒ ์ฌ์ดํธ์ด๋ฏ๋ก ์คํธ๋ฆฌ๋ฐ ์ ๊ณต์ฌ ๊ณต๊ธ์ด ํ์
  - TMDB์ ์ํ๋ง๋ค ์คํธ๋ฆฌ๋ฐ ์ ๋ณด๋ฅผ ์ ๊ณต
    - TMDB API๋ฅผ ํ์ฉํด ํด๋น ๋ฐ์ดํฐ ์ถ๊ฐ ์ ์ฅ ๋ฐ ๊ฐ๊ณต์ฒ๋ฆฌ ์งํ(1๋ N ๊ด๊ณ)
    - ์คํธ๋ฆฌ๋ฐ ์ ์ ์ฌ์ดํธ ๋งํฌ๋ ์ถ๊ฐ๋ก ์ ๊ณต

![image-20221203113226229](update.assets/image-20221203113226229.png)

```python
# movies/views.py

@api_view(['GET'])
def movie_provieder(request, movie_id):
    '''
    ์คํธ๋ฆฌ๋ฐ(๋ทํ๋ฆญ์ค, ์์ฑ  ๋ฑ)์ ๋ํ ์ ๋ณด๋ฅผ ๋ถ๋ฌ์ค๋ ํจ์
    '''
    providers = get_list_or_404(Provider, movie_id = movie_id)
    serializer = ProviderSerializer(providers, many=True)
    return Response(serializer.data)

# movies/models.py
# ์คํธ๋ฆฌ๋ฐ(๋ทํ๋ฆญ์ค, ์์ฑ  ๋ฑ) ์ ๋ณด๋ฅผ ๋ด๋ ํ์ด๋ธ
class Provider(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    provider_link = models.CharField(max_length=200)
    provider_logo_path = models.CharField(max_length=200)
```



- ๋ก๊ณ  ์ด๋ฏธ์ง ์ถ๋ ฅ ๋ฐ ํด๋ฆญ ์ ๋งํฌ๋ก ์ด๋!

![image-20221203113347356](update.assets/image-20221203113347356.png)



### ๐ 11.29(ํ๋กํ ์ด๋ฏธ์ง ์์ฑ, ์์ , ์ญ์ /ํ๋ก์ฐ, ํ๋ก์,๋๊ธ,๋ฆฌ๋ทฐ, ํ๋กํ์ ์ด๋ฏธ์ง ์ ์ฉ)

- ํ๋กํ ์ด๋ฏธ์ง๊ฐ ์์ ์ ์ ์ ์์ ์ํต๊ณผ ์น๋ฐ๊ฐ์ด ๋์์ง
  - ๊ผญ ๊ตฌํํ๊ณ  ์ถ์ ๊ธฐ๋ฅ์ด์๋ค
  - ์ด๋ฏธ์ง๋ฅผ ์ ์ฅํ๊ธฐ ์ํ form.py ์์ฑ/ models์ค์ / views.py์์ ์ ์ฅ ๊ตฌํ์ด ์ด๋ ค์ ๋ค.
  - ์ ์ ๋ง๋ค ๊ณ ์ ์ ํ๋กํ ์ด๋ฏธ์ง๋ฅผ ๊ฐ์ง๊ณ  ์๊ณ  ์ค๋ณต ์ ์ฅ๋์ง ์๊ฒ ๊ตฌํ ์งํ!
    - ์ด๊ธฐ ์ด๋ฏธ์ง ์์ฑ ์ ์ ์  ์์ด๋๊ฐ ์์ธ ์ด๋ฏธ์ง ํ์ผ์ ๋ณต์ฌ!
    - ํด๋น ๋ณต์ฌ๋ ํ์ผ๋ง ์์ /์ญ์  ๋๋๋ก ์งํ
    - ์ญ์  ์ default ์ด๋ฏธ์ง๋ค ์ค์ ํ๋๋ก ๋๋ค ์ ์ฅ๋๋๋ก ๊ตฌํ

![image-20221203114521663](update.assets/image-20221203114521663.png)

```python
##### accounts/forms.py
# profile image ํ์ผ์ ๋ด๊ธฐ ์ํ form
class UserForm(forms.ModelForm):
    
    class Meta:
        model = get_user_model()
        fields = ('profile_image',)

# accounts/models.py
# ํ๋ก์ฐ, ํ๋กํ ์ด๋ฏธ์ง ๊ธฐ๋ฅ์ ์ํ ๋ชจ๋ธ
class User(AbstractUser):
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    profile_image = models.ImageField(blank=True, upload_to='images/')

###### accounts/views.py

@api_view(['GET', 'POST', 'DELETE'])
def profile_image(request, user_id):
    '''
    ํ๋กํ ์ด๋ฏธ์ง๋ฅผ ์ ์ฅํ๊ณ  ์ด๊ธฐํํ๊ณ  ๋ถ๋ฌ์ค๋ ํจ์
    
    [๋ฌธ์ ์ฌํญ 1]: ์ด๋ฏธ์ง๋ฅผ ์ ์ฅํ๋ฉด ๊ธฐ์กด ์ฌ์ง์ ์ง์์ง ์ ์๊ฒ ๊ตฌํํ๋ ๊ฒ ์ด๋ ค์ ๋ค. -> POST ์์ฒญ์ ํ์ ๋์๋ ๊ธฐ์กด ๋ฐ์ดํฐ๋ฅผ ๋ฏธ๋ฆฌ ์ญ์ ํ๊ณ  ์ ์ฅํ๋ ์ชฝ์ผ๋ก ํด๊ฒฐ
     โป django-cleanup์ ํ์ํ๋ ค๊ณ  ํ์์ผ๋, ๊ธฐ์กด ํ๋กํ์ ์ง์๋ฒ๋ฆฌ๋ ํ์์ด ๋ฐ์
     
    [๋ฌธ์ ์ฌํญ 2]: default ์ด๋ฏธ์ง๋ฅผ ๋ค์ํ ์์ผ๋ก ํํํ๊ณ  ์ถ์ด์ ๋ฐ๋ก defaults ํด๋ ๋ด์ ๊ธฐ๋ณธ ํ๋กํ ์ด๋ฏธ์ง๋ฅผ ์๋ณ๋ก 4๊ฐ ์ ์ฅํด์ฃผ๊ณ  ๋๋ค์ผ๋ก ์ ๊ณตํ๋ ๊ฒ์ผ๋ก ๋ณ๊ฒฝ
    
    [๋ฌธ์ ์ฌํญ 3]: ๊ฐ์ฅ ์ด๊ธฐ์ ์ด๋ฏธ์ง๋ default ์ด๋ฏธ์ง๋ฅผ ๋ณต์ฌํด์ ํ์ผ๋ช์ ์ ์ ๋ช์ ํฉ์ณ์ image ํด๋ ๋ด์ ์ ์ฅ(์ ์ ๋ณ ์ฌ์ง ๊ตฌ๋ถ ๊ฐ๋ฅ)
    '''
    User = get_user_model()
    me = request.user
    person = User.objects.get(id=user_id)
    if request.method == 'GET':
        if person.profile_image:
            serializer = UserSerializer(person)
        else:
            ran = random.sample(range(0, 4), 1)
            image = './media/defaults/default' + str(ran[0]) + '.png'
            shutil.copy(image, './media/images/default'+ str(ran[0]) + person.username + '.png')
            person.profile_image = 'images/default'+ str(ran[0]) + person.username + '.png'
            person.save()
            serializer = UserSerializer(person)
        return Response(serializer.data)
    elif request.method == 'POST':
        if me == person:
            person.profile_image.delete()
            form = UserForm(request.POST, request.FILES, instance=person)
            # print(form.is_valid())
            # print(request.FILES.get('image'))
            if form.is_valid():
                form = form.save(commit=False)
                form.profile_image=request.FILES.get('image')
                form.save()
                # print(form)
            serializer = UserSerializer(person)
            return Response(serializer.data)
    elif request.method == 'DELETE':
        person.profile_image.delete()
        ran = random.sample(range(0, 4), 1)
        image = './media/defaults/default' + str(ran[0]) + '.png'
        # shutil.copy(image, './media/images/default'+ str(ran[0]) + '.png')
        # person.profile_image = 'images/default'+ str(ran[0]) + '.png'
        shutil.copy(image, './media/images/default'+ str(ran[0]) + person.username + '.png')
        person.profile_image = 'images/default'+ str(ran[0]) + person.username + '.png'
        person.save()
        serializer = UserSerializer(person)
        return Response(serializer.data)
```





- ๋ฏธ๋์ด ํ์ผ์ ๊ธฐ๋ณธ ํ๋กํ์ ์๊น๋ณ๋ก ์ถ๊ฐ ์ ์ฅ
  - ๋์ ์ธ ๋๋์ด ๋ณด์ด๋๋ก ๊ตฌํ
  - ๋๋ค์ผ๋ก ์๊น์ด ์ํ์ง๊ฒ ํจ
  - ๊ฐ ์ ์ ์ ์ด๋ฏธ์ง๊ฐ ์์ฑ/์์ /์ญ์  ์ ํ๋์ ์ด๋ฏธ์ง๋ง ์ ์ฅ๋๋๋ก ๊ตฌํ(DB ์ ์ฅ ํจ์จํ!)

![image-20221203113456435](update.assets/image-20221203113456435.png)

```vue
//ProfileView.vue

getProfileImage() {
        axios({
        method: 'post',
            url: `${API_URL}/accounts/wantid/`,
            data: {
            username: this.userName
            },
            headers: { 
              Authorization: `Token ${this.$store.state.token}`
            },
      })
      .then((res) => {
        const id = res.data.userid
        axios({
        method: 'get',
        url: `${API_URL}/accounts/profile_image/${id}/`,
        data: this.image,
        headers: { 
          'Content-Type': 'multipart/form-data',
              Authorization: `Token ${this.$store.state.token}`
            },
        })
        .then((res) => {
          this.profileImageUrl=`${API_URL}${res.data.profile_image}`
        })
        .catch((err) => {
          console.log(err)
        })
        })
      .catch((err) => {
        console.log(err)
      })
    },
    SaveImage() {
      if (!this.image) {
        swal("ํ์ผ ์์!", "ํ์ผ์ ์๋ก๋ ํด์ฃผ์ธ์!", "warning");
      } else {
        axios({
        method: 'post',
            url: `${API_URL}/accounts/wantid/`,
            data: {
            username: this.userName
            },
            headers: { 
              Authorization: `Token ${this.$store.state.token}`
            },
      })
      .then((res) => {
        const id = res.data.userid
        axios({
        method: 'post',
        url: `${API_URL}/accounts/profile_image/${id}/`,
        data: this.image,
        headers: { 
          'Content-Type': 'multipart/form-data',
              Authorization: `Token ${this.$store.state.token}`
            },
        })
        .then((res) => {
          this.profileImageUrl=`${API_URL}${res.data.profile_image}`
          swal("์๋ก๋ ์๋ฃ!", "ํ๋กํ ํธ์ง์ด ์๋ฃ๋์์ต๋๋ค", "success");
        })
        .catch((err) => {
          console.log(err)
        })
        })
      .catch((err) => {
        console.log(err)
      })
      }
```



### ๐ 12.01(์ ๊ตญ ์ํ๊ด ์์น ์นด์นด์ค๋งต ๊ตฌํ!)

- ํ๊ตญ๋ฌธํ์ ๋ณด์์ ๊ตญ๋ด ์ํ๊ด ์์น ๋ฐ์ดํฐ๋ฅผ ์์ํ์ผ๋ก ๋ฐ์์์ DB์ ์ ์ฅ
  - csvํ์ผ์ DB์ ์ ์ฅํ๋ ๋ฐฉ๋ฒ์ ํ์ต!

![image-20221203114432347](update.assets/image-20221203114432347.png)



```python
#movies/views.py

def csv_to_DB(request):
'''
example.csv์ด๋ผ๋ ์ํ๊ด ๊ณต๊ณต๋ฐ์ดํฐ๋ฅผ ํตํด csv๋ฅผ DB์ ์ ์ฅํ๋ ํจ์
[๋ฌธ์ ์ฌํญ]: ์๋์ ๊ฒฝ๋๋ ๋ฌธ์๋ก ์ ์ฅ๋๊ธฐ ๋๋ฌธ์ ์ถํ์ ์ซ์๋ก ๋ฐ๊ฟ์ผํ๋ค.
'''
     data = pandas.read_csv("./movies/example.csv")
     filter_data = data.filter(items=['POI_NM', 'CTPRVN_NM','SIGNGU_NM', 'LEGALDONG_NM', 'LC_LO', 'LC_LA'])
     total_cnt = len(filter_data)
     for i in range(total_cnt):
         Cinema.objects.create(
             name = filter_data.loc[i][0],
             metropolitan_city = filter_data.loc[i][1],
             district = filter_data.loc[i][2],
             region = filter_data.loc[i][3],
             latitude = filter_data.loc[i][4],
             altitude = filter_data.loc[i][5]
             )
```



- ์, ๊ตฌ, ๋ ๋ณ๋ก ๋ฐ์ดํฐ๋ฅผ ๋ถ๋ฌ์์ ํด๋น ์ํ๊ด ์์น๋ฅผ ๋ถ๋ฌ์ค๋ ํจ์ ์์ฑ
  - ์ ์ ํ ์ ํด๋น ์์ ๊ด๋ จ๋ ๊ตฌ๊ฐ ๋ถ๋ฌ์์ง๊ณ , ๊ตฌ๊ฐ ์ ํ๋๋ฉด ๊ด๋ จ๋ ๋์ด ๋ถ๋ฌ์์ง๋๋ก ์ค์ 
  - ๊ตฌ์ฒด์ ์ธ ์์น๋ฅผ ์ค์ ํ  ์ ์๊ฒ ํ์ฌ ์๋น์๊ฐ ์ํ๋ ์ง์ญ์ ํ์ธํ  ์ ์๋๋ก ๊ตฌํ

![image-20221203114834094](update.assets/image-20221203114834094.png)

```python
#movies/views.py

@api_view(['GET'])
def cinema_list(request):
    '''
    ์ฃผ์ด์ง 3๊ฐ์ง์ ์ฃผ์ ๋ฐ์ดํฐ(๊ด์ญ์, ๊ตฌ, ๋)๋ฅผ ํตํด ํด๋น ์ํ๊ด ์ฐพ์์ ๋ฐํํ๋ ํจ์
    [์์ด๋์ด]: ์นด์นด์ค ๋งต์ ํํํ  ๋ ์ง์ญ ๋จ์๋ก ๊ตฌ๋ถํ๊ณ  ์ถ์๋ค.
    '''
    metropolitan_city = request.GET.get('metropolitan_city')
    district = request.GET.get('district')
    region = request.GET.get('region')
    cinema = Cinema.objects.filter(metropolitan_city=metropolitan_city).filter(district=district).filter(region=region)
    if len(cinema) == 1:
        serializer = CinemaSerializer(cinema[0])
        return Response(serializer.data)
    elif len(cinema) >= 2:
        serializer = CinemaSerializer(cinema, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def district_list(request, city):
    '''
    city๋ฅผ ์ ํํ๊ณ  ๋์ ๋ฐ์ดํฐ๋ฅผ ๋ฐ์ ํ์ district์ ์ต์์ ๊ฒฐ์ ํด์ฃผ๊ธฐ ์ํ ํจ์
    ์๋ฅผ ๋ค์ด, ๊ฐ์๋๊ฐ ์ ํ๋์ด์ง๋ฉด ๊ทธ์ ๋ฐ๋ฅธ ๊ตฌ๋ค์ด ์ต์์ ๋ํ๋๋๋ก ํ  ์์ 
    '''
    cinemas = Cinema.objects.filter(metropolitan_city=city)
    selectcity = cinemas.order_by('district')
    results = selectcity.values_list('district', flat=True).distinct()
    return Response(results)


@api_view(['GET'])
def region_list(request, city, district):
    '''
    ๊ด์ญ์์ ๊ตฌ์ ์ ๋ณด๋ฅผ ๋ฐํ์ผ๋ก ๋๋ฅผ ํ์ํ๋ ํจ์
    [๋ฌธ์ ์ํฉ] ๊ด์ญ์์ ํํฐ๋ฅผ ๊ฑธ์ด์ฃผ์ง ์์ผ๋ ๋ค๋ฅธ ๊ด์ญ์์ ๊ฐ์ ๊ตฌ๊ฐ ๊ฒน์ณ์ ๋์ค๋ ๊ฒฝ์ฐ๊ฐ ์๊ฒผ์๋ค
    '''
    cinemas = Cinema.objects.filter(metropolitan_city=city).filter(district=district)
    selectcity = cinemas.order_by('region')
    results = selectcity.values_list('region', flat=True).distinct()
    return Response(results)
```



- ์นด์นด์ค๋งต API ํ์ฉ
  - ์นด์นด์ค๋งต API ์ฌ์ดํธ์ ์์ธํ๊ฒ ์ฌ์ฉ๋ฐฉ๋ฒ์ด ๋ช์๋จ
  - Vue์ ์ ํฉํ ํํ๋ก ํจ์ ๋ณํ
  - ๋ง์ปค๋ก ์์น๊ฐ ์ฐํ ์ ์๊ฒ ์ถ๊ฐ ๊ตฌํ ์งํ
- ์ด๋ ค์ ๋ ์ 
  - JavaScript ๋ฌธ๋ฒ์ด ์ต์์น ์์์ ํ๋  ์ฌํญ์ด ๋ง์์(์ถ๊ฐ ํ์ต ํ์!)

```vue
initMap() {
      const Lng = Number(this.Lng);
      const Lat = Number(this.Lat);
      const container = document.getElementById("map");
      const options = {
        center: new kakao.maps.LatLng(Lat, Lng),
        level: 3,
      };
      this.map = new kakao.maps.Map(container, options);
      // console.log(this.map)

      // ํ์ฌ ํ์๋์ด ์๋ marker ์ ๊ฑฐ
      if (this.markers.length > 0) {
        this.markers.forEach((item) => {
          item.setMap(null);
        });
      }

      // ๋ง์ปค ์ด๋ฏธ์ง ๋ถ๋ฌ์ค๊ธฐ
      const imageSrc =
        "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png";
      const imageSize = new kakao.maps.Size(24, 35);
      // ๋ง์ปค ์ด๋ฏธ์ง๋ฅผ ์์ฑํฉ๋๋ค
      const markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize);
      this.markerPositions.forEach((position) => {
        const marker = new kakao.maps.Marker({
          map: this.map,
          position: position.latlng,
          // title: position.title,
          image: markerImage,
        });
        // ๋ง์ปค์ ํ์ํ  ์ธํฌ์๋์ฐ๋ฅผ ์์ฑํฉ๋๋ค
        const infowindow = new kakao.maps.InfoWindow({
          content: `<span style="color: black;">${position.title}</span>`, // ์ธํฌ์๋์ฐ์ ํ์ํ  ๋ด์ฉ
        });
        // ๋ง์ปค์ mouseover ์ด๋ฒคํธ์ mouseout ์ด๋ฒคํธ๋ฅผ ๋ฑ๋กํฉ๋๋ค
        // ์ด๋ฒคํธ ๋ฆฌ์ค๋๋ก๋ ํด๋ก์ ๋ฅผ ๋ง๋ค์ด ๋ฑ๋กํฉ๋๋ค
        // for๋ฌธ์์ ํด๋ก์ ๋ฅผ ๋ง๋ค์ด ์ฃผ์ง ์์ผ๋ฉด ๋ง์ง๋ง ๋ง์ปค์๋ง ์ด๋ฒคํธ๊ฐ ๋ฑ๋ก๋ฉ๋๋ค
        kakao.maps.event.addListener(
          marker,
          "mouseover",
          this.makeOverListener(this.map, marker, infowindow)
        );
        kakao.maps.event.addListener(
          marker,
          "mouseout",
          this.makeOutListener(infowindow)
        );
        this.markers.push(marker);
      });

      //๋ง์ปค๊ฐ 2๊ฐ ์ด์์ผ ๋ ๋ชจ๋ ๋ณด์ผ ์ ์๊ฒ ์ง๋ ์ด๋
      const bounds = this.markerPositions.reduce(
        (bounds, position) => bounds.extend(position.latlng),
        new kakao.maps.LatLngBounds()
      );
      this.map.setBounds(bounds);
    },
    // ์ธํฌ์๋์ฐ๋ฅผ ํ์ํ๋ ํด๋ก์ ๋ฅผ ๋ง๋๋ ํจ์์๋๋ค
    makeOverListener(map, marker, infowindow) {
      return function () {
        infowindow.open(map, marker);
      };
    },
    // ์ธํฌ์๋์ฐ๋ฅผ ๋ซ๋ ํด๋ก์ ๋ฅผ ๋ง๋๋ ํจ์์๋๋ค
    makeOutListener(infowindow) {
      return function () {
        infowindow.close();
      };
    },
```



### ๐ 12.03(๊ฒ์ ์์ง ์ต์ ํ + ํ์คํธ ์๋ํฐ ์ถ๊ฐ ์คํจ)

- ๐ฅ**๋ฌธ์ ์ ** **๋ฐ๊ฒฌ**
  - @input์ ํ์ฉํ  ๊ฒฝ์ฐ ์ ์ ์ ์๋ ฅ๋ง๋ค axios๊ฐ ํธ์ถ๋์ด ๋ฐ์ดํฐ๊ฐ ์ค๋ณต๋์ด ํ์๋จ
    - ์๋ฅผ ๋ค์ด brad pitt ๋ฐฐ์ฐ๋ฅผ ์๋ ฅํ์์ง๋ง, b/br/brad ๊ฐ๊ฐ์ ๋ฐ์ดํฐ๊ฐ ๋์ค์ ์ฒ๋ฆฌ๋์ด ํ๋ฉด์ ํ์๋์ด ๋ฒ๋ฆผ
  - ๋ก๋ฉ ์คํผ๋๊ฐ ์์ด์ ํ๋ฉด์ด ๋ฐ์ํ๊ณ  ์๋์ง ์ ์ ์์!

- ๐ **์ต์ ํ** **์งํ**
  - setTimeํจ์๋ฅผ ํตํด ์๋ ฅ ํ **2.5์ด** ๋ค์ axios ์์ฒญ์ด ์งํ๋๋๋ก ํจ<span style="color:red;">**(delay๊ฐ ํต์ฌ!!)**</span>
    - ๋จ, axios ์์ฒญ ์ ์๋ ฅ๋ ๊ฐ๊ณผ ํ์ฌ ๊ฒ์์๋ ฅ์ ๋ค์ด๊ฐ ๊ฐ์ด ๋์ผํ  ๊ฒฝ์ฐ๋ง axios ์์ฒญ์ ๋ณด๋
    - ํ์ฌ ๊ฒ์์ด๊ฐ ์์ฒญ ์๋ ฅ๊ณผ ๋ค๋ฅธ ๊ฒฝ์ฐ์๋ ๋ฐ๋ก returnํ๊ฒ ์งํํ์ฌ ํธ์ถ๋์ง ์๋๋ก ํจ
  - ๋ค๋ฆ๊ฒ ์๋ต๋ ๋ฐ์ดํฐ๊ฐ ํ์ฌ ๋ฐ์ดํฐ๋ฅผ ๋ฎ์ด์์ด๋ ๊ฒฝ์ฐ!!!(์ค๋ณต ์๋ฐ์ดํธ ์ ๊ฑฐ!)
    - ๋ค๋ฆ๊ฒ ์๋ต๋ ๋ฐ์ดํฐ์ ๊ฒ์์ด ์๋ ฅ๊ฐ์ด ํ์ฌ์ ์๋ ฅ๊ฐ๊ณผ ์ผ์นํ  ๊ฒฝ์ฐ์๋ง ๋ฎ์ด์ฐ๊ธฐ ์ธ์ 
    - ํ์ฌ์ ๊ฒ์์ด๊ฐ ์๋ต๋์ด์จ ๊ฒ์์ด์ ๋ค๋ฅผ ๊ฒฝ์ฐ ๋ฎ์ด์ฐ์ง ์๊ณ  ๊ทธ๋ฅ return
  - ๋ก๋ฉ ์คํผ๋ ์ถ๊ฐ
    - axios ์  isLoading์ true๋ก ํ์ฌ ๋ก๋ฉ๋ฐ๊ฐ ๋๋๋ก ํ์์ผ๋ฉฐ ์๋ต ํ์ false๋ก ๋ก๋ฉ๋ฐ๋ฅผ ์ ๊ฑฐ

![image-20221203115242852](update.assets/image-20221203115242852.png)

```vue
methods: {
    SearchData(e) {
      //๋ญ๊ฐ๋ฅผ ๊ฑธ์ด์ค๋ค.์๊ฐ ์ง์ฐ -> ์ต์ ํ ํ์//
      //๋์์ด ๋งค๋๋ฝ์ง ์๊ณ  ๋ฒ๊ทธ๊ฐ ์๊ธธ ์ ์์//
      
      const inputData = e.target.value
      this.currentData = e.target.value

      //์๋ ฅ์ด ์์ ๊ฒฝ์ฐ ๋ก๋ฉ ๋ฒํผ์ด ์๊ธฐ์ง ์๊ฒ ์ค์ //
      if (inputData.length === 0) {
        this.isLoading = false
        this.searchMovies = []
      } else {
        // ์๋ ฅ ํ 2500ms์ ๊ฐ๊ฒฉ์ ์ฃผ๊ณ  ๊ฒ์์ ์งํ//
        // ํ์ฌ ์๋ ฅ๊ฐ๊ณผ ์ฐพ์ ์๋ ฅ๊ฐ์ด ๋ค๋ฅด๋ฉด ์งํ ํ์ง ์๋๋ค(๊ณ ๊ฐ์ด ๊ณ์ ์๋ ฅ ์ค์ด๋ผ๋ ์๋ฏธ) //
        setTimeout(() => {
          if (inputData === this.currentData) {
            this.isLoading = true
            axios({
              method: 'get',
              url: `${API_URL}/api/v1/movies/search/${inputData}/`
          })
          .then((res) => {
            // ์ด์ ์ ์์ฒญํ ๋ฐ์ดํฐ๊ฐ ๋ค๋ฆ๊ฒ ํ๋ฉด์ ์ถ๋ ฅ๋  ๊ฒฝ์ฐ๊ฐ ์์//
            // ์์ ์ ์๋ ฅ๊ฐ์ด ํ์ฌ์ ์๋ ฅ๊ฐ๊ณผ ๊ฐ์ผ๋ฉด ํ๋ฉด์ ์ถ๋ ฅํ๊ณ , ๊ทธ๋ ์ง ์์ผ๋ฉด ๋ฐ๋ก returnํ  ์ ์๊ฒ ํ๋ฉด์ ๋ค๋ฆ๊ฒ ์ถ๋ ฅ๋๋ ๊ฒ์ ๋ฐฉ์ง//
            if (inputData === this.currentData) {
              this.searchMovies = res.data
              this.isLoading = false
            } else {
              return
            }
          })
          .catch(() => {
              this.searchMovies = []
          })
          } else {
            return
          }
        }, 2500)
      }
      }}
```

- ํ์คํธ ์๋ํฐ ๊ธฐ๋ฅ ์ถ๊ฐ ์คํจ
  - ํ์คํธ ์๋ํฐ ๊ธฐ๋ฅ์ ์ถ๊ฐํ์์ง๋ง, ํด๋น ๊ฐ์ด ์ถ๋ ฅ๋  ๋ `<p> <strong>`๊ณผ ๊ฐ์ ๋ฌธ๋ฒ๋ค์ด ๋ฌธ์์ด๋ก ํ์๋จ
  - ์ถํ ์๊ฐ๋  ๋ ํ์ธ์ด ํ์ํจ!!



### ๐ 12.05(์ธํผ๋ํธ ์คํฌ๋กค ์ต์ ํ)

- ๐ฅ**๋ฌธ์ ์ **
  - ์ธํผ๋ํฐ ์คํฌ๋กค ๊ธฐ๋ฅ์ด ์กด์ฌํ์์ผ๋ ๋ชจ๋  ์ํ๋ฐ์ดํฐ๋ฅผ ํ๊บผ๋ฒ์ ๋ถ๋ฌ์จ ํ limit์ ํตํด 30๊ฐ์ฉ ๋ณด์ฌ์ฃผ๋ ๋ฐฉ์์ด์ด์ ๋นํจ์จ ์ ์ธ ๋ฐฉ๋ฒ
    - 3000์ฌ๊ฐ์ ๋ฐ์ดํฐ๋ฅผ ๋ถ๋ฌ์ค๋๋ฐ 5.7์ด ์์๋จ
    - ์ฅ๋ฅด๋ณ ์ํ ๊ฒ์, ๋ฉ์ธ ์ํ ํ์ด์ง์ ํด๋น ์๊ฐ๋ค์ด ์์๋์ด ๋ก๋ฉ์ด ๊ธธ์ด์ง
- ๐ข**ํด๊ฒฐ** **๋ฐฉ๋ฒ**
  - ๋ชจ๋  ๋ฐ์ดํฐ๊ฐ ์๋ ์ธํผ๋ํฐ ์คํฌ๋กค๋ง์ด ์คํ๋  ๋์๋ง axios ์์ฒญ์ ๋ณด๋ด ํ์ํ ๋ฐ์ดํฐ๋ง ๋ฐ์์ด
    - ํ์ด์ง๋น ์ฝ 67ms์ผ๋ก ์๋ ํฅ์!
  - ํ์ด์ง๋น 15๊ฐ์ ๋ฐ์ดํฐ๋ฅผ ๊ฐ์ ธ์ด
    - ์ฅ๋ฅด ๊ฒ์ ํ์ด์ง์๋ ํด๋น ์ฌํญ ๊ตฌํ ์๋ฃ

![image-20221205122849676](update.assets/image-20221205122849676.png)

![image-20221205123244036](update.assets/image-20221205123244036.png)

```vue
// MovieView.vue
// page๋น 15๊ฐ์ฉ ๋ฐ์ดํฐ๋ฅผ ๋ถ๋ฌ์ค๊ฒ ๊ตฌํ ์งํ

infiniteHandler($state) {
      this.page += 1
      axios({
        method: 'GET',
        url: `${API_URL}/api/v1/movies/list/${this.page}/`
      })
      .then((res) => {
        // console.log(res.data)
        // console.log(res.data.length)
        setTimeout(() => {
          if (res.data.length > 0) {
            res.data.forEach((movie) => {
              this.movies_infinite.push(movie)
            })
            // console.log(this.movies_infinite)
            $state.loaded()
          } else {
            $state.complete()
          }
        }, 1000)
      })
      .catch((err) => {
        console.log(err)
      })
    },
```

```python
#movies/views.py

@api_view(['GET'])
def movie_list(request, page):
    '''
    ๋จ์ํ ์ํ ๋ชจ๋  ์ ๋ณด๋ฅผ ๋์ดํ๋ ํจ์
    [๋ฌธ์ ์ฌํญ]: 3000์ฌ๊ฐ์ ์ํ ๋ฐ์ดํฐ๋ฅผ ํ๊บผ๋ฒ์ ๋ถ๋ฌ์ค๋ฉด 5.7์ด์ ๋ก๋ฉ ์๊ฐ์ด ํ์ํ๋ค.(ํ์ํ  ๋๋ง๋ค ์ ๋ณด๋ฅผ ๋ถ๋ฌ์ค๋ ์ต์ ํ ํ์)
    -> ์๊ฐ ์ง์ฐ์ ์ค์ผ ํ์๊ฐ ์์
    -> ํ์ด์ง๋ฅผ ํ์ฉํ์ฌ 15๊ฐ์ฉ ๋ฐ์ดํฐ๊ฐ ์๋ต๋๋๋ก ์ต์ ํ ์๋ฃ!
    '''
    start_idx = 15 * page
    end_idx = 15 * (page + 1)
    movies = get_list_or_404(Movie)[start_idx: end_idx]
    serializer = MovieListSerializer(movies, many=True)
    # print(serializer.data)
    return Response(serializer.data)
```

