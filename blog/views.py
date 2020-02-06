from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect


# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

#-------------------------------------------------Postフォームを新しく作るには、PostForm()を呼び出し、テンプレートに出力
def post_new(request):
    if request.method == "POST":    # 新しく投稿された時
        form = PostForm(request.POST)   

        # フォームの値が正しいかどうか
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()     #フォームの値が有効なら保存
            return redirect('post_detail', pk=post.pk)      #post_detail.htmlに移動

    else :  #投稿がなければフォームを新しく作る
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form})


#--------------------------------------------------- 投稿したものを編集する
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

