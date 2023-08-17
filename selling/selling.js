async function fetchProductDetails() {
    // 임시 데이터 (실제 API 호출로 대체해야 함)
    const sample_data = {
      id: 1, 
      name: "특별기획 아삭상추 300g", 
      img: "https://via.placeholder.com/250", 
      price: "9,000원", 
      description: "안심하고 드실 수 있도록 무농약으로 정성껏 키웠습니다.  국내에서 가장 건강한 방식으로 만든 맛 좋은 상추입니다."


    };
  
    return Promise.resolve(sample_data); // 임시 데이터 반환 (테스트용)
    
    // 실제 API 호출 사용 예시
    // const response = await fetch('https://example.com/api/product/1');
    // return response.json();
  }
  
  async function loadProductDetails() {
    const productDetailsContainer = document.getElementById('product-details');
    const product = await fetchProductDetails();
    const productElement = createProductElement(product);
    productDetailsContainer.appendChild(productElement);
  }
  
  function createProductElement(product) {
    const productWrapper = document.createElement('div');
    productWrapper.className = 'mb-4 row';
  
    // 이미지 영역 생성
    const imageWrapper = document.createElement('div');
    imageWrapper.className = 'col-md-6';
    const productImage = document.createElement('img');
    productImage.src = product.img;
    productImage.className = 'img-fluid';
    imageWrapper.appendChild(productImage);
    
    // 상세 정보 영역 생성
    const detailsWrapper = document.createElement('div');
    detailsWrapper.className = 'col-md-6';
    const productName = document.createElement('h5');
    productName.textContent = product.name;
    const productPrice = document.createElement('p');
    productPrice.className = 'price';
    productPrice.textContent = product.price;
    const productDescription = document.createElement('p');
    productDescription.textContent = product.description;
    detailsWrapper.appendChild(productName);
    detailsWrapper.appendChild(productPrice);
    detailsWrapper.appendChild(productDescription);
  
    productWrapper.appendChild(imageWrapper);
    productWrapper.appendChild(detailsWrapper);
    return productWrapper;
  }
  
  loadProductDetails();
  

