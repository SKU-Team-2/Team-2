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
  
    const imageWrapper = document.createElement('div');
    imageWrapper.className = 'col-md-6';
    const productImage = document.createElement('img');
    productImage.src = product.img;
    productImage.className = 'img-fluid';
    imageWrapper.appendChild(productImage);
    
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
  

//자바스크립트 댓글 기능 

        // 댓글 수정 기능
        function editComment(editBtn) {
          editBtn.addEventListener('click', (e) => {
              const commentEl = e.target.closest('.mb-3');
              const commentTextEl = commentEl.querySelector('.comment-text');
              
              const newValue = prompt('댓글을 수정하세요.', commentTextEl.textContent);
              if (newValue !== null) {
                  commentTextEl.textContent = newValue;
              }
          });
      }

      // 댓글 삭제 기능
      function deleteComment(deleteBtn) {
          deleteBtn.addEventListener('click', (e) => {
              if (confirm('댓글을 삭제하시겠습니까?')) {
                  const commentEl = e.target.closest('.mb-3');
                  commentEl.remove();
              }
          });
      }

      document.querySelectorAll('.edit-btn').forEach(editBtn => editComment(editBtn));
      document.querySelectorAll('.delete-btn').forEach(deleteBtn => deleteComment(deleteBtn));

      // 댓글 작성 기능
      const commentForm = document.querySelector('.comment-form');
      const submitCommentBtn = document.getElementById('submit-comment');
      const commentInput = document.getElementById('comment-input');

      submitCommentBtn.addEventListener('click', () => {
          const commentText = commentInput.value;

          if (commentText === '') {
              alert('댓글 작성란이 공백입니다. 댓글을 입력하세요.');
              return;
          }

          const newCommentTemplate = `
              <div class="mb-3">
                  <div class="d-flex align-items-start slider-content">
                      <img src="./sellingimg/user.png" class="profile-image" alt="사용자 프로필 이미지">
                      <div class="ms-2">
                          <p class="mb-0"><strong>익명</strong></p>
                          <p class="mb-0 comment-text">${commentText}</p>
                          <small>작성일: ${new Date().toISOString().slice(0, 10)}</small>
                          <button class="edit-btn btn bg-light text-black mb-0">수정</button>
                          <button class="delete-btn btn bg-light text-black mb-0">삭제</button>
                      </div>
                  </div>
              </div>
          `;

          commentForm.insertAdjacentHTML('afterend', newCommentTemplate);
          commentInput.value = '';


          const newCommentEl = commentForm.nextElementSibling;
          const newEditBtn = newCommentEl.querySelector('.edit-btn');
          const newDeleteBtn = newCommentEl.querySelector('.delete-btn');

          newEditBtn.classList.add('edit-button'); 
          newDeleteBtn.classList.add('delete-btn'); 
          
          editComment(newEditBtn);
          deleteComment(newDeleteBtn);
      });

