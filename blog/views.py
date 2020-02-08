from django.shortcuts import render
from django.utils import timezone
from .models import Post, Comment
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required   #ログイン機能用



# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

#-------------------------------------------------Postフォームを新しく作るには、PostForm()を呼び出し、テンプレートに出力
@login_required #ログインしてたら
def post_new(request):
    if request.method == "POST":    # 新しく投稿された時
        form = PostForm(request.POST)   

        # フォームの値が正しいかどうか
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()     #フォームの値が有効なら保存
            return redirect('post_detail', pk=post.pk)      #post_detail.htmlに移動

    else :  #投稿がなければフォームを新しく作る
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form})


#--------------------------------------------------- 投稿したものを編集する
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

#--------------------------------------------------- 草稿用
@login_required
def post_draft_list(request):
    #草稿だけを集めて、作られた順に並べる
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

#--------------------------------------------------- 投稿用
@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

#--------------------------------------------------- 投稿されたら投稿時間と保存を行う
def publish(self):
    self.published_date = timezone.now()
    self.save()

#--------------------------------------------------- 投稿削除用
@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


#--------------------------------------------------- コメント追加用
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

#--------------------------------------------------- コメント承認用
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


#--------------------------------------------------- コメント削除用
@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

