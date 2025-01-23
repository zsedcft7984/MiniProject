
// 아이템 삭제 처리
document.querySelectorAll('.remove-item').forEach(button => {
    button.addEventListener('click', function() {
        const itemId = this.getAttribute('data-item-id');
        const xhr = new XMLHttpRequest();
        xhr.open('POST', `/web/remove_item/${itemId}`, true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                const data = JSON.parse(xhr.responseText);
                if (data.success) {
                    const cartItemElement = document.getElementById('cart-item-' + itemId);
                    if (cartItemElement) {
                        cartItemElement.remove();
                    }
                    alert("아이템이 삭제되었습니다.");
                    // 총 가격 업데이트
                    document.querySelector('.total-price').textContent = `총 가격: ₩ ${data.new_total_price}`;
                    window.location.reload();

                } else {
                    alert("아이템 삭제에 실패했습니다.");
                }
            }
        };
        xhr.send(JSON.stringify({ item_id: itemId }));

        if (cartCount) {
            const xhr = new XMLHttpRequest();
            xhr.open('GET', '/web/get_cart_count', true);
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    const data = JSON.parse(xhr.responseText);
                    cartCount.textContent = data.cart_count || 0;  // 기본값 0
                } else if (xhr.readyState === 4) {
                    console.error('Error fetching cart count:', xhr.status);
                }
            };
            xhr.send();
        }
    });
});