import numpy as np
from utils.initialization import initialize_positions
from utils.levy_flight import levy_flight

def swo(search_agents_no, Tmax, ub=None, lb=None, dim=None, fobj=None, tol=1e-10, max_stall=300):
    # Устанавливаем границы поиска, если они не заданы
    if ub is None:
        ub = 512 * np.ones(dim)
    if lb is None:
        lb = -512 * np.ones(dim)

    # Инициализация переменных
    Best_SW = np.zeros(dim)  # Лучшая позиция (обновляется в процессе)
    Best_score = np.inf  # Лучшая оценка (обновляется в процессе)
    Convergence_curve = np.zeros(Tmax)  # Мощность сходимости
    neval = 0  # Число оценок
    neval_per_function = {fobj.__name__: 0}  # Число оценок для функции

    TR = 0.5  # Вероятность использования первой стратегии
    Cr = 0.3  # Вероятность кроссовера
    N_min = 20  # Минимальное количество агентов

    # Инициализация позиций агентов
    Positions = initialize_positions(search_agents_no, dim, ub, lb)
    # Оценка для каждой позиции
    SW_Fit = np.array([fobj(Positions[i]) for i in range(search_agents_no)])
    neval += search_agents_no
    neval_per_function[fobj.__name__] += search_agents_no

    # Инициализация лучшей позиции и лучшей оценки после первой итерации
    Best_score = np.min(SW_Fit)
    Best_SW = Positions[np.argmin(SW_Fit)].copy()

    t = 0
    stall_count = 0
    prev_best_score = Best_score

    # Основной цикл
    while t < Tmax and stall_count < max_stall:
        # Динамическое изменение параметра а
        a = 2 - 2 * (t / Tmax)
        a2 = -1 - 1 * (t / Tmax)
        k = 1 - t / Tmax
        JK = np.random.permutation(search_agents_no)

        # Если выбирается первая стратегия охоты
        if np.random.rand() < TR:
            for i in range(search_agents_no):
                r1, r2, r3, p = np.random.rand(4)
                C = a * (2 * r1 - 1)  # Коэффициент, влияющий на изменение позиции
                l = (a2 - 1) * np.random.rand() + 1  # Леви-флайт коэффициент
                L = levy_flight(dim)  # Применение Леви-Полета для случайных шагов
                vc = np.random.uniform(-k, k, dim)  # Вектор случайных изменений
                rn1 = np.random.randn()  # Случайное нормальное число
                O_P = Positions[i].copy()  # Сохранение старой позиции

                # Обновление позиции агента с применением первой стратегии охоты
                for j in range(dim):
                    if i < k * search_agents_no:  # Агент с различными стратегиями
                        if p < (1 - t / Tmax):  # Если агент использует охоту
                            if r1 < r2:  # Охота по принципу "погоня"
                                m1 = abs(rn1) * r1
                                Positions[i, j] += m1 * (Positions[JK[1], j] - Positions[JK[2], j])  # Погоня за жертвой
                            else:  # Взаимодействие с окружающей средой
                                B = 1 / (1 + np.exp(l))  # Элемент взаимодействия
                                m2 = B * np.cos(l * 2 * np.pi)
                                Positions[i, j] = Positions[JK[i], j] + m2 * (lb[j] + np.random.rand() * (ub[j] - lb[j]))
                        else:  # Агент использует другой способ обновления
                            if r1 < r2:
                                Positions[i, j] += C * abs(2 * np.random.rand() * Positions[JK[3], j] - Positions[i, j])
                            else:
                                Positions[i, j] *= vc[j]
                    else:  # Обновление для агентов, находящихся ближе к лучшему решению
                        if r1 < r2:
                            Positions[i, j] = Best_SW[j] + np.cos(2 * l * np.pi) * (Best_SW[j] - Positions[i, j])
                        else:
                            Positions[i, j] = Positions[JK[1], j] + r3 * abs(L[j]) * (Positions[JK[1], j] - Positions[i, j]) + (1 - r3) * (np.random.rand() > np.random.rand()) * (Positions[JK[3], j] - Positions[JK[2], j])

                # Применение границ для позиции агента
                Positions[i] = np.clip(Positions[i], lb, ub)
                # Оценка позиции агента
                SW_Fit1 = fobj(Positions[i])
                neval += 1
                neval_per_function[fobj.__name__] += 1

                # Если новая позиция лучше, обновляем лучшую позицию
                if SW_Fit1 < SW_Fit[i]:
                    SW_Fit[i] = SW_Fit1
                    if SW_Fit1 < Best_score:
                        Best_score = SW_Fit1
                        Best_SW = Positions[i].copy()
                else:
                    Positions[i] = O_P  # Возвращаем прежнюю позицию, если результат хуже

        # Если выбирается вторая стратегия спаривания
        else:
            for i in range(search_agents_no):
                l = (a2 - 1) * np.random.rand() + 1  # Модификация для спаривания
                SW_m = np.zeros(dim)
                O_P = Positions[i].copy()

                # Разница между лучшими и текущими агентами
                v1 = Positions[JK[1]] - Positions[i] if SW_Fit[JK[1]] < SW_Fit[i] else Positions[i] - Positions[JK[1]]
                v2 = Positions[JK[2]] - Positions[JK[3]] if SW_Fit[JK[2]] < SW_Fit[JK[3]] else Positions[JK[3]] - Positions[JK[2]]

                rn1, rn2 = np.random.randn(2)  # Случайные нормальные числа

                # Спаривание агентов для обмена информацией
                for j in range(dim):
                    SW_m[j] = Positions[i, j] + (np.exp(l)) * abs(rn1) * v1[j] + (1 - np.exp(l)) * abs(rn2) * v2[j]
                    # Применение кроссовера
                    if np.random.rand() < Cr:
                        Positions[i, j] = SW_m[j]

                # Применение границ для позиции агента
                Positions[i] = np.clip(Positions[i], lb, ub)
                # Оценка позиции агента
                SW_Fit1 = fobj(Positions[i])
                neval += 1
                neval_per_function[fobj.__name__] += 1

                # Если новая позиция лучше, обновляем лучшую позицию
                if SW_Fit1 < SW_Fit[i]:
                    SW_Fit[i] = SW_Fit1
                    if SW_Fit1 < Best_score:
                        Best_score = SW_Fit1
                        Best_SW = Positions[i].copy()
                else:
                    Positions[i] = O_P  # Возвращаем прежнюю позицию, если результат хуже

        # Обновление сходимости
        t += 1
        Convergence_curve[t - 1] = Best_score

        # Проверка на стагнацию (если изменения в лучшей оценке очень малы)
        if abs(prev_best_score - Best_score) < tol:
            stall_count += 1
        else:
            stall_count = 0

        prev_best_score = Best_score

        # Адаптивное уменьшение количества агентов
        search_agents_no = max(N_min, int(N_min + (search_agents_no - N_min) * ((Tmax - t) / Tmax)))

    return Best_score, Best_SW, Convergence_curve[:t], neval, neval_per_function
