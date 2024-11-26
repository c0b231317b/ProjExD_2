import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたrectが画面内か外かを判定する
    引数：こうかとんRect or 爆弾Rect
    戻り値：横方向・縦方向の真理値タプル（True：画面内／False：画面外）
    """
    yoko = True
    tate = True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


# def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
#     """
#     サイズの異なる爆弾Surfaceを要素としたリストと加速度リストを返す
#     引数：なし
#     戻り値：爆弾タプル
#     """



def game_over(screen: pg.Surface) -> None:
    """
    ゲームオーバー時に，半透明の黒い画面上に「Game Over」と表示し，    泣いているこうかとん画像を貼り付ける関数
    引数：こうかとんSurface or 爆弾Surface
    """
    # ブラックアウト（全画面）
    blackout = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(blackout, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))
    blackout.set_alpha(30)
    blackout_sc = blackout.get_rect()
    screen.blit(blackout,blackout_sc)
    # 「Game Over」テキスト 表示
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(txt,txt_rct)
    # 泣いているここうかとん 表示
    kk_naki_img = pg.image.load("fig/8.png")
    kk_naki_rct = kk_naki_img.get_rect(center = (WIDTH//2-180, HEIGHT//2))
    screen.blit(kk_naki_img,kk_naki_rct)
    kk_naki_rct = kk_naki_img.get_rect(center = (WIDTH//2+180, HEIGHT//2))
    screen.blit(kk_naki_img,kk_naki_rct)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0
    # pr_2
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = 5, 5
    # pr_１
    DELTA = {
        pg.K_UP : (0,-5), 
        pg.K_DOWN : (0, 5),
        pg.K_LEFT : (-5, 0),
        pg.K_RIGHT : (5, 0),
    }
    # # 爆弾のサイズ変更 関数
    # bb_imgs, bb_accs = init_bb_imgs()
    # avx = vx*bb_accs[min(tmr//500, 9)]
    # bb_img = bb_imgs[min(tmr//500, 9)]



    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        # #pr_5
        # if kk_rct.colliderect(bb_rct):
        #     print("ゲームオーバー")
        #     return

        # ゲームオーバー関数 呼び出し
        if kk_rct.colliderect(bb_rct):
            game_over(screen)
            pg.display.update()
            time.sleep(5)
            return
        
        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)
        # pr_3  こうかとんが画面内に閉じ込める
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(bb_img, bb_rct)
        bb_rct.move_ip(vx, vy)       
        # pr_3 爆弾 画面内
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(kk_img, kk_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

