let cart;
if(localStorage.getItem('cart')==null){
    cart ={}
}
else{
    cart = JSON.parse(localStorage.getItem('cart'))
    document.querySelector('#cart').textContent = Object.keys(cart).length
}

document.querySelectorAll('.cart').forEach((button)=>{
    button.addEventListener('click',(e)=>{
        var idstr = button.id.toString();
        if (cart[idstr] !== undefined){
            cart[idstr] += 1;
        }
        else{
            cart[idstr] = 1
        }
        localStorage.setItem('cart',JSON.stringify(cart));
        document.querySelector('#cart').textContent = Object.keys(cart).length;
    })
})