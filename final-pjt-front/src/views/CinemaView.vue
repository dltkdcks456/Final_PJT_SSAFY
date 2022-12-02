<template>
  <div>
    <div
      style="
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
      "
    >
        <h1>영화관 위치 정보</h1>
      <div style="display: flex; justify-content: space-around; width:650px;">
        <div>
          <select
            class="form-select mb-3"
            style="width:200px; margin-top:15px;"
            v-model="select0"
            @change="getSelect1"
          >
            <option selected>선택</option>
            <option
              v-for="(city, index) in metropolitan_city"
              :key="index"
              :value="city"
            >
              {{ city }}
            </option>
          </select>
        </div>
        <div>
          <select
            class="form-select mb-3"
            style="width:180px; margin-top:15px;"
            v-model="select1"
            @change="getSelect2"
          >
            <option selected>선택</option>
            <option
              v-for="(district, index) in districts"
              :key="`ss-${index}`"
              :value="district"
            >
              {{ district }}
            </option>
          </select>
        </div>
        <div>
          <select style="width:100px; margin-top:15px;" class="form-select mb-3" v-model="select2">
            <option selected>선택</option>
            <option
              v-for="(region, index) in regions"
              :key="`aa-${index}`"
              :value="region"
            >
              {{ region }}
            </option>
          </select>
        </div>
        <div>
          <button class="btn btn-danger m-3" @click="getCinema">
            데이터 출력
          </button>
        </div>
      </div>
      <div>
        <div v-if="Lat" id="map"></div>
        <img
          v-if="!Lat"
          src="https://blog.kakaocdn.net/dn/EKIAk/btroaNkDBsZ/81pirx8L2TAnnUOUmfeEK1/img.png"
          id="default-img"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

export default {
  name: "CinemaView",
  data() {
    return {
      map: null,
      select0: "선택",
      select1: "선택",
      select2: "선택",
      metropolitan_city: [
        "강원도",
        "경기도",
        "경상남도",
        "경상북도",
        "광주광역시",
        "대구광역시",
        "대전광역시",
        "부산광역시",
        "서울특별시",
        "세종특별자치시",
        "울산광역시",
        "인천광역시",
        "전라남도",
        "전라북도",
        "제주특별자치도",
        "충청남도",
        "충청북도",
      ],
      districts: [],
      regions: [],
      Lat: null,
      Lng: null,
      markerPositions: [],
      markers: [],
    };
  },
  methods: {
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

      // 현재 표시되어 있는 marker 제거
      if (this.markers.length > 0) {
        this.markers.forEach((item) => {
          item.setMap(null);
        });
      }

      // 마커 이미지 불러오기
      const imageSrc =
        "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png";
      const imageSize = new kakao.maps.Size(24, 35);
      // 마커 이미지를 생성합니다
      const markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize);
      this.markerPositions.forEach((position) => {
        const marker = new kakao.maps.Marker({
          map: this.map,
          position: position.latlng,
          // title: position.title,
          image: markerImage,
        });
        // 마커에 표시할 인포윈도우를 생성합니다
        const infowindow = new kakao.maps.InfoWindow({
          content: `<span style="color: black;">${position.title}</span>`, // 인포윈도우에 표시할 내용
        });
        // 마커에 mouseover 이벤트와 mouseout 이벤트를 등록합니다
        // 이벤트 리스너로는 클로저를 만들어 등록합니다
        // for문에서 클로저를 만들어 주지 않으면 마지막 마커에만 이벤트가 등록됩니다
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

      //마커가 2개 이상일 때 모두 보일 수 있게 지도 이동
      const bounds = this.markerPositions.reduce(
        (bounds, position) => bounds.extend(position.latlng),
        new kakao.maps.LatLngBounds()
      );
      this.map.setBounds(bounds);
    },
    // 인포윈도우를 표시하는 클로저를 만드는 함수입니다
    makeOverListener(map, marker, infowindow) {
      return function () {
        infowindow.open(map, marker);
      };
    },
    // 인포윈도우를 닫는 클로저를 만드는 함수입니다
    makeOutListener(infowindow) {
      return function () {
        infowindow.close();
      };
    },
    getCinema() {
      axios({
        method: "get",
        url: `${API_URL}/api/v1/cinema/`,
        params: {
          metropolitan_city: this.select0,
          district: this.select1,
          region: this.select2,
        },
      })
        .then((res) => {
          if (res.data.length > 1) {
            this.Lng = res.data[0].latitude;
            this.Lat = res.data[0].altitude;
            const positions = [];
            res.data.forEach((movie) => {
              let movieLng = Number(movie.latitude);
              let movieLat = Number(movie.altitude);
              positions.push({
                title: movie.name,
                latlng: new kakao.maps.LatLng(movieLat, movieLng),
              });
            });
            this.markerPositions = positions;
          } else {
            // 데이터가 하나일 경우 사용
            this.Lng = res.data.latitude;
            this.Lat = res.data.altitude;
            const positions = [];
            positions.push({
              title: `${res.data.name}`,
              latlng: new kakao.maps.LatLng(this.Lat, this.Lng),
            });
            this.markerPositions = positions;
          }
        })
        .then(() => {
          this.initMap();
        })
        .catch((err) => {
          console.log(err);
        });
    },
    getSelect1() {
      axios({
        method: "get",
        url: `${API_URL}/api/v1/cinema/district/${this.select0}/`,
      })
        .then((res) => {
          this.districts = res.data;
          this.regions = []
          // console.log(this.district)
        })
        .catch((err) => {
          console.log(err);
        });
    },
    getSelect2() {
      // console.log(this.select1)
      axios({
        method: "get",
        url: `${API_URL}/api/v1/cinema/region/${this.select0}/${this.select1}/`,
      })
        .then((res) => {
          this.regions = res.data;
          // console.log(res.data)
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
  mounted() {
    if (!window.kakao || !window.kakao.maps) {
      const script = document.createElement("script");
      script.src = `//dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${process.env.VUE_APP_KAKAOMAP_KEY}`;
      script.addEventListener("load", () => {
        // console.log("loaded", window.kakao)
        kakao.maps.load(this.initMap);
      });
      document.head.appendChild(script);
    } else {
      // console.log("이미 로딩됨: ", window.kakao)
      this.initMap();
    }
  },
};
</script>

<style>
#map {
  width: 500px;
  height: 500px;
}

#default-img {
  margin-top: 80px;
  margin-bottom: 90px;
  width: 350px;
  /* height: 500px; */
}
</style>