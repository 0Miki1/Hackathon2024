using System.Linq;

namespace LeltarParositasResultValidator
{
    internal class Program
    {
        static List<MintaAdat> GetAdatok(string pathToMintaAdatok)
        {
            //var mintaAdatok = File.ReadAllLines(pathToMintaAdatok);
            var mintaAdatok = File.ReadAllLines("tanito_adat.csv");

            return mintaAdatok
                .Skip(1)
                .Select(x => x.Split(';'))
                .Select(s => new MintaAdat
                {
                    HianyId = int.Parse(s[0]),
                    HianyEszkozNev = s[1],
                    HianyMuszakiCsoportId = s[2],
                    HianyMuszakiCsoportNev = s[3],
                    TobbletId = int.Parse(s[4]),
                    TobbletEszkozNev = s[5],
                    TobbletMuszakiCsoportId = s[6],
                    TobbletMuszakiCsoportNev = s[7]
                })
                .ToList();
        }

        static List<EredmenyAdat> GetEredmenyAdatok(string pathToEredmenyAdatok)
        {
            //var eredmenyAdatok = GetAdatok(pathToEredmenyAdatok);
            var eredmenyAdatok = GetAdatok("javasolt_parok.csv");

            return eredmenyAdatok
                .GroupBy(eredMenyAdat => eredMenyAdat.HianyId)
                .Select(group => new EredmenyAdat
                {
                    HianyId = group.Key,
                    Javaslatok = group.ToList()
                })
                .ToList();
        }

        static double GetTalalatiArany(List<MintaAdat> mintaAdatok, List<EredmenyAdat> eredmenyAdatok)
        {
            mintaAdatok = mintaAdatok.OrderBy(x => x.HianyId).ToList();
            eredmenyAdatok = eredmenyAdatok.OrderBy(x => x.HianyId).ToList();

            double talalatok = 0;

            eredmenyAdatok.ForEach(eredmenyAdat =>
            {
                bool talalat = mintaAdatok
                    .Where(mintaAdat => mintaAdat.HianyId == eredmenyAdat.HianyId)
                    .Where(mintaAdat => eredmenyAdat.Javaslatok.Any(eredmenyA => eredmenyA.TobbletId == mintaAdat.TobbletId))
                    .Any();

                if (talalat)
                {
                    talalatok++;
                }
                else
                {
                    Console.WriteLine($"Nem talált: {eredmenyAdat.HianyId}");
                }
            });

            return talalatok / eredmenyAdatok.Count;
        }

        static void Main(string[] args)
        {
            Console.Write("Minta adatok: ");
            string mintaAdatPath = Console.ReadLine();

            Console.Write("Eredmeny adatok: ");
            string eredmenyAdatPath = Console.ReadLine();

            var mintaAdatok = GetAdatok(mintaAdatPath);

            var eredmenyAdatok = GetEredmenyAdatok(eredmenyAdatPath);

            double talatiArany = GetTalalatiArany(mintaAdatok, eredmenyAdatok);

            Console.WriteLine($"Talalati arány: {Math.Round(talatiArany * 100, 2)}%");
        }
    }
}
