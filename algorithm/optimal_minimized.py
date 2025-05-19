def find_optimal_alpha(obj, bounds, tol=1e-2, max_iter=50):
    
    a, b = bounds
    for _ in range(max_iter):
        mid = (a + b) / 2
        f_mid = obj(mid)
        f_a = obj(a)
        f_b = obj(b)
        
        # 检查收敛
        if abs(b - a) < tol:
            break
        
        # 更新搜索范围
        if f_mid < f_a and f_mid < f_b:
            # 如果 mid 是最小值，缩小范围
            if obj(mid - tol) < obj(mid + tol):
                b = mid
            else:
                a = mid
        elif f_a < f_b:
            b = mid
        else:
            a = mid
    
    return (a + b) / 2


if __name__ == '__main__':
    # for test
    def obj(alpha):
        return alpha**2 + 2*alpha + 1
    
    bounds = (0, 1)
    alpha = find_optimal_alpha(obj, bounds)
    print(f'The optimal alpha is {alpha:.4f}')