// function setDetailImage(input) {
//   if (input.files && input.files[0]) {
//     var reader = new FileReader();
//     reader.onload = function (e) {
//       document.getElementById("img").src = e.target.result;
//     };
//     reader.readAsDataURL(input.files[0]);
//   } else {
//     document.getElementById("img").src = "";
//   }
// }

// function readInputFile(e) {
//   var sel_files = [];

//   sel_files = [];
//   $(".carousel-item").empty();

//   var files = e.target.files;
//   var fileArr = Array.prototype.slice.call(files);
//   var index = 0;

//   fileArr.forEach(function (f) {
//     if (!f.type.match("image/.*")) {
//       alert("이미지 확장자만 업로드 가능합니다.");
//       return;
//     }
//     if (files.length < 11) {
//       sel_files.push(f);
//       var reader = new FileReader();
//       reader.onload = function (e) {
//         var html = `<a id=img_id_${index}><img src=${e.target.result} data-file=${f.name} /></a>`;
//         $("carousel-item").append(html);
//         index++;
//       };
//       reader.readAsDataURL(f);
//     }
//   });
//   if (files.length > 4) {
//     alert("최대 3장까지 업로드 할 수 있습니다.");
//   }
// }

// $("#real-input").on("change", readInputFile);

// const express = require("express");
// const app = express();

// // CORS 설정
// app.use((req, res, next) => {
//   // 특정 도메인의 요청을 허용하도록 설정
//   res.header(
//     "Access-Control-Allow-Origin",
//     "file:///Users/a82108/Desktop/SeeNear/post.html"
//   );
//   res.header(
//     "Access-Control-Allow-Headers",
//     "Origin, X-Requested-With, Content-Type, Accept"
//   );
//   next();
// });

// // 라우트 및 서버 실행 코드
// // ...

// const port = 3000;
// app.listen(port, () => {
//   console.log(`서버가 포트 ${port}에서 실행 중입니다.`);
// });

// function setDetailImage(f) {
//   var file = f.files;

//   // 확장자 체크
//   if (!/\.(gif|jpg|jpeg|png)$/i.test(file[0].name)) {
//     alert("gif, jpg, png 파일만 선택해 주세요.\n\n현재 파일 : " + file[0].name);

//     // 선택한 파일 초기화
//     f.outerHTML = f.outerHTML;

//     document.getElementById("carousel-inner").innerHTML = "";
//   } else {
//     // FileReader 객체 사용
//     var reader = new FileReader();

//     // 파일 읽기가 완료되었을때 실행
//     reader.onload = function (rst) {
//       document.getElementById("carousel-inner").innerHTML =
//         '<img src="' + rst.target.result + '">';
//     };

//     // 파일을 읽는다
//     reader.readAsDataURL(file[0]);
//   }
// }

function setDetailImage(event) {
  const imageInput = event.target;
  const imagePreview = document.getElementById("imagePreview");

  if (imageInput.files && imageInput.files[0]) {
    const file = imageInput.files[0];
    const reader = new FileReader();

    reader.onload = function (e) {
      imagePreview.src = e.target.result;
      imagePreview.style.display = "block";
    };

    reader.readAsDataURL(file);
  }
}
