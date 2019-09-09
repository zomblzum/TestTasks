using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;

namespace ReadFileAndCount
{
    class Program
    {
        static void Main(string[] args)
        {
            string path = args[0];
            string line;

            if (File.Exists(path))
            {
                StreamReader file = null;
                try
                {   
                    // Чтение файла
                    file = new StreamReader(path, Encoding.UTF8);
                    // Построчная проверка
                    while ((line = file.ReadLine()) != null)
                    {
                        // Массив слов в строке
                        string[] words = line.ToLower()
                                             .Split(new char[] { ' ', '.', ',', '!', '?', ';', ':' }, StringSplitOptions.RemoveEmptyEntries);

                        // Группируем, считаем и сортируем
                        var result = words.GroupBy(x => x)
                                          .OrderByDescending(x => x.Count())
                                          .ThenBy(x => x.Key)
                                          .Select(x => new {Word = x.Key, Frequency = x.Count() });

                        // Вывод результата
                        foreach (var item in result) {
                            Console.WriteLine(item.Word + " " + item.Frequency);
                        }
                    }
                }
                catch
                {
                    Console.WriteLine("Ошибка при обработке файла");
                }

                if (file != null)
                {
                    file.Close();
                }
            }
            Console.WriteLine("Обработка файла завершена, нажмите кнопку чтобы закрыть окно");
            Console.ReadKey(true);
        }
    }
}