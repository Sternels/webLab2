addToCart = document.querySelectorAll('.addtocart')
addToCartShop = document.querySelectorAll('.addtocart-shop')
cartDelete = document.querySelectorAll('.cart-delete')
chktbtn = document.querySelector('.chkt-btn')

let data = new FormData();
data.append('csrfmiddlewaretoken', document.getElementById('csrftoken').value);
addToCart.forEach((item)=>{
    data.append('id', item.id)
    console.log(data.get('id'))

    item.addEventListener('click', (e)=>{
        e.stopPropagation()
        count = document.getElementById('qty')
        data.append('count', count.value)
        fetch('/product-create/',{
            method:'POST',
            body: data
        }).then(res=>
            res.json()
        ).then(res=>{
           document.querySelector('.cart-count').innerHTML=`(${res.length})`

        })
        window.alert('Товар добавлен')

    })
})

addToCartShop.forEach((item)=>{

    item.addEventListener('click', (e)=>{
        let data = new FormData();
        data.append('csrfmiddlewaretoken', document.getElementById('csrftoken').value);

        e.stopPropagation()
        data.append('id', e.target.id)
        console.log(e.target)
        count = 1
        data.append('count', count)
        fetch('/product-create/',{
            method:'POST',
            body: data
        }).then(res=>
            res.json()
        ).then(res=>{
           document.querySelector('.cart-count').innerHTML=`(${res.length})`

        })
        window.alert('Товар добавлен')

    })
})

cartDelete.forEach((item)=>{

    item.addEventListener('click', (e)=>{
        let data = new FormData();
        data.append('csrfmiddlewaretoken', document.getElementById('csrftoken').value);

        e.stopPropagation()
        data.append('id', e.target.id.slice(3))
        e.target.parentNode.parentNode.parentNode.removeChild(e.target.parentNode.parentNode)
        fetch('/product-delete/',{
            method:'POST',
            body: data
        }).then(res=>res.json()).then(res=>{
            document.querySelector('.totalsum').innerHTML='$'+res.total
            document.querySelector('.cart-count').innerHTML=`(${res.length})`
        })
        window.alert('Товар удален')

    })
})

chktbtn.addEventListener('click', ()=>{
    let data = new FormData();
    sum = Number(document.querySelector('.totalsum').innerHTML.slice(1))
    if (sum>0){
    data.append('csrfmiddlewaretoken', document.getElementById('csrftoken').value);
     data.append('fname',document.getElementById('fname').value)
     data.append('lname',document.getElementById('lname').value)
     data.append('mail',document.getElementById('mail').value)
     data.append('addr',document.getElementById('addr').value)
     data.append('zip',document.getElementById('zip').value)
     data.append('comment',document.getElementById('comment').value)
     data.append('total',sum)
    fetch('/order-create/', {
        method: 'POST',
        body:data
    }).then(res=>{
        document.querySelector('.totalsum').innerHTML = $0
        document.querySelector('.cart-count').innerHTML=`(0)`

    })

    }


    window.alert('Товры оплачены')
})