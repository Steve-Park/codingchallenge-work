# 과제 1
## Product 의 검색 기능 추가
* 검색 기능 추가를 위하여 하기 소스에 아래와 같이 수정/추가
* product.html - Bootstrap 참조하여 inputbox 구성
```
<div class="row mt-5">
  <div class="col-12">
    <div class="input-group mb-3">
      <input type="text" class="form-control" placeholder="상품명" name="input-search" id="input-search"
        onkeyup="enterkey();">
      <button class="btn btn-outline-secondary" type="button" id="button-search" onclick="do_search()">검색</button>
    </div>
  </div>
</div>
```
* product.html - 검색어 전달을 위한 JavaScript 추가
```
  function do_search() {
    s = document.querySelector('#input-search').value;
    url = (s ? '/product/?s=' + s : '/product/');
    window.location.href = url;
  };

  function enterkey() {
    if (window.event.keyCode == 13) {
      // 엔터키가 눌렸을 때 실행할 내용
      do_search();
    };
  };
```
* product.views.py - QuerySet 조작을 위한 get_queryset Method Override
```
class ProductList(ListView):
    ...

    def get_queryset(self):
        qs = super().get_queryset()
        s = self.request.GET.get('s')
        return qs if (s is None) else qs.filter(name__icontains=unquote(s)).order_by('id')
```
# 과제 2
## Product 페이지의 Pagenation 개선
* product.html - Bootstrap 및 QueryString 유지를 위하여 아래와 같이 수정
```
    <nav>
      <ul class="pagination justify-content-center">
        {% if page_obj.has_previous %}
        <li class="page-item">
          <a class="page-link" href="?page={{ page_obj.previous_page_number }}&s={{ request.GET.s }}">이전으로</a>
        </li>
        {% else %}
        <li class="page-item disabled">
          <a class="page-link" href="#">이전으로</a>
        </li>
        {% endif %}
        <li class="page-item active">
          <a class="page-link" href="#"> {{ page_obj.number }} / {{ page_obj.paginator.num_pages }} </a>
        </li>
        {% if page_obj.has_next %}
        <li class="page-item">
          <a class="page-link" href="?page={{ page_obj.next_page_number }}&s={{ request.GET.s }}">다음으로</a>
        </li>
        {% else %}
        <li class="page-item disabled">
          <a class="page-link" href="#">다음으로</a>
        </li>
        {% endif %}
      </ul>
    </nav>
```
